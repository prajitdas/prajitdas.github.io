import os
from pathlib import Path
from bs4 import BeautifulSoup

def secure_file(filepath):
    print(f"Securing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # 1. Add CSP Meta Tag
        if not soup.find('meta', attrs={'http-equiv': 'Content-Security-Policy'}):
            csp_tag = soup.new_tag('meta')
            csp_tag.attrs['http-equiv'] = 'Content-Security-Policy'
            csp_tag.attrs['content'] = "default-src 'none'; script-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'self'; form-action 'none';"

            head = soup.find('head')
            if head:
                # Append to end of head
                head.append(csp_tag)
            else:
                # Create head if missing
                head = soup.new_tag('head')
                if soup.html:
                    soup.html.insert(0, head)
                else:
                    soup.insert(0, head)
                head.append(csp_tag)
                print("  Added missing <head> tag with CSP.")

        # 2. Upgrade HTTP to HTTPS for known domains
        secure_domains = [
            'arxiv.org', 'dx.doi.org', 'doi.org', 'www.igi-global.com',
            'ebiquity.umbc.edu', 'ceur-ws.org', 'search.proquest.com',
            'www.lri.fr'
        ]

        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http://'):
                for domain in secure_domains:
                    if domain in href:
                        new_href = href.replace('http://', 'https://', 1)
                        a['href'] = new_href
                        print(f"  Upgraded link: {href} -> {new_href}")
                        break

        # 3. Add rel="noopener noreferrer" to external links
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Simple check for external links (http/https and not same domain)
            if href.startswith('http') and 'prajitdas.github.io' not in href:
                rel = a.get('rel', [])
                if isinstance(rel, str):
                    rel = rel.split()

                added = False
                if 'noopener' not in rel:
                    rel.append('noopener')
                    added = True
                if 'noreferrer' not in rel:
                    rel.append('noreferrer')
                    added = True

                if added:
                    a['rel'] = rel
                    # print(f"  Secured link: {href}")

        with open(filepath, 'w', encoding='utf-8') as f:
            # prettify() can alter layout significantly, str(soup) is safer for preserving some structure
            # but BeautifulSoup might reorder attributes.
            f.write(str(soup))
            print(f"  Saved {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    # Resolve paths relative to this script
    script_dir = Path(__file__).parent.resolve()
    # Go up two levels to root, then to assets...
    repo_root = script_dir.parent.parent
    pub_dir = repo_root / 'assets' / 'docs' / 'publications'

    files_to_secure = [
        'my-publications.html',
        'my-publications-bib.html',
        'my-publications-abstracts.html'
    ]

    print(f"Scanning directory: {pub_dir}")

    for filename in files_to_secure:
        filepath = pub_dir / filename
        if filepath.exists():
            secure_file(filepath)
        else:
            print(f"Warning: {filepath} not found.")

if __name__ == '__main__':
    main()
