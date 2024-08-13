import os
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from bs4 import BeautifulSoup

class LanguageSwitcherPlugin(BasePlugin):
    def on_page_content(self, html, page, config, files):
        # Create the HTML for the language switcher
        switcher_html = '''
        <div class="language-switcher">
            <button id="language-button">Language</button>
            <div id="language-dropdown" class="dropdown-content">
                <a href="#" data-lang="en">English</a>
                <a href="#" data-lang="pt">Brazilian Portuguese</a>
            </div>
        </div>
        '''

        # Inject the language switcher into the page content
        soup = BeautifulSoup(html, 'html.parser')
        body_tag = soup.body
        if body_tag:
            body_tag.insert(0, BeautifulSoup(switcher_html, 'html.parser'))
            return str(soup)

        return html

    def on_post_build(self, config):
        # Ensure the language switcher JS and CSS are copied to the output directory
        output_dir = config['site_dir']
        js_path = os.path.join(output_dir, 'js')
        css_path = os.path.join(output_dir, 'css')

        os.makedirs(js_path, exist_ok=True)
        os.makedirs(css_path, exist_ok=True)

        with open(os.path.join(js_path, 'language-switcher.js'), 'w') as f:
            f.write(self.get_js_content())

        with open(os.path.join(css_path, 'language-switcher.css'), 'w') as f:
            f.write(self.get_css_content())

    def get_js_content(self):
        return '''
        document.addEventListener("DOMContentLoaded", function() {
            const languageButton = document.getElementById("language-button");
            const languageDropdown = document.getElementById("language-dropdown");

            languageButton.addEventListener("click", function() {
                languageDropdown.classList.toggle("show");
            });

            document.querySelectorAll("#language-dropdown a").forEach(function(link) {
                link.addEventListener("click", function(event) {
                    event.preventDefault();
                    const selectedLanguage = link.getAttribute("data-lang");
                    const currentPath = window.location.pathname;

                    if (selectedLanguage === "en") {
                        window.location.href = "/en" + currentPath.replace("/pt", "");
                    } else if (selectedLanguage === "pt") {
                        window.location.href = "/pt" + currentPath.replace("/en", "");
                    }
                });
            });

            window.addEventListener("click", function(event) {
                if (!event.target.matches('#language-button')) {
                    if (languageDropdown.classList.contains('show')) {
                        languageDropdown.classList.remove('show');
                    }
                }
            });
        });
        '''

    def get_css_content(self):
        return '''
        .language-switcher {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
            display: inline-block;
        }

        #language-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
        }

        #language-button:hover {
            background-color: #45a049;
        }

        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #f9f9f9;
            min-width: 160px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 1;
            right: 0;
        }

        .dropdown-content a {
            color: black;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
        }

        .dropdown-content a:hover {
            background-color: #f1f1f1;
        }

        .language-switcher:hover .dropdown-content {
            display: block;
        }
        '''

