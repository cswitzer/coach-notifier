from lxml import etree
import requests

from consts import COACH_PRODUCT_SITEMAP, LOCAL, BASE_DIR


class CoachProductSitemapCrawler:
    def __init__(self):
        self.url = COACH_PRODUCT_SITEMAP

    def search_urls(self, product_name: str) -> list[str]:
        """Search for product URLs containing the specified product name."""
        product_name = product_name.strip()
        if not product_name:
            return []

        xml_content = self._fetch_sitemap()
        return self._parse_sitemap(xml_content, product_name)

    def _fetch_sitemap(self) -> str:
        """Fetch the sitemap XML content."""
        if LOCAL:
            file_path = BASE_DIR / "sitemap_0-product.xml"
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()

        try:
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch sitemap from {self.url}: {e}") from e

    def _parse_sitemap(self, xml_content: str, product_name: str) -> list[str]:
        """Parse the sitemap XML content and return product URLs.

        Example XML snippet:
        ```
        <url>
            <loc>
                https://www.coach.com/products/coach-leather-cleaner/223.html
            </loc>
            <lastmod>2025-07-08T01:20:39+00:00</lastmod>
            <changefreq>daily</changefreq>
            <priority>0.5</priority>
            <image:image>
                <image:loc>https://coach.scene7.com/is/image/Coach/223_mti_a0</image:loc>
                <image:caption>Coach Leather Cleaner</image:caption>
                <image:title>MTI</image:title>
            </image:image>
            <image:image>
                <image:loc>https://coach.scene7.com/is/image/Coach/223_mti_a1</image:loc>
                <image:caption>Coach Leather Cleaner</image:caption>
                <image:title>MTI</image:title>
            </image:image>
        </url>
        ```
        """
        namespaces = {
            # For name clashes such as "loc", which is in the url namespace and image namespace
            "sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "image": "http://www.google.com/schemas/sitemap-image/1.1",
        }

        root = etree.fromstring(xml_content.encode("utf-8"))
        matching_urls = []

        for url_elem in root.findall("sitemap:url", namespaces):
            # no use searching if there is no url
            loc_elem = url_elem.find("sitemap:loc", namespaces)
            if loc_elem is None:
                continue

            # the image contains the product name
            url = loc_elem.text
            image_elems = url_elem.findall("image:image", namespaces)
            if not image_elems:
                continue

            for image_elem in image_elems:
                if self._image_matches_product(image_elem, product_name, namespaces):
                    matching_urls.append(url)
                    break

        return matching_urls

    def _image_matches_product(
        self, image_elem: etree.Element, product_name: str, namespaces: dict[str, str]
    ) -> bool:
        """Check if the image caption matches the product name."""
        caption_elem = image_elem.find("image:caption", namespaces)
        if caption_elem is None or caption_elem.text is None:
            return False
        xml_product_name = caption_elem.text
        return product_name.lower() == xml_product_name.lower()
