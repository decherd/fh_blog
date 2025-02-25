from fasthtml.common import *
from monsterui.all import *
from pathlib import Path
from datetime import datetime
import yaml
import os
from bs4 import BeautifulSoup


app, rt = fast_app(hdrs=(Theme.zinc.headers(), HighlightJS(langs=["python", "bash", "yaml", "json"], light="atom-one-dark")), live=True)

def load_posts():
    """Load all posts from the posts directory"""
    posts_dir = Path("posts")
    posts = []
    
    for post_file in sorted(posts_dir.glob("*.md"), reverse=True):
        with open(post_file, "r", encoding="utf-8") as f:
            # Read frontmatter and content
            content = f.read()
            
            # Split frontmatter from content
            _, frontmatter, content = content.split("---", 2)
            
            # Parse frontmatter
            metadata = yaml.safe_load(frontmatter)
            
            # Create post object
            post = {
                "slug": post_file.stem,
                "content": content.strip(),
                **metadata
            }
            posts.append(post)
    
    # Sort posts by date, newest first
    return sorted(posts, key=lambda x: datetime.strptime(x["date"], "%B %d, %Y"), reverse=True)

def SocialLink(icon, text, url):
    """Creates a social media link with icon"""
    return A(
        DivLAligned(
            UkIcon(icon),
            P(text, cls=TextPresets.md_weight_sm)
        ),
        href=url,
        target="_blank",
        rel="noopener noreferrer",
        cls="hover:text-gray-500 duration-200"
    )

def BlogPostCard(post):
    """Creates a card for a blog post preview"""
    return A(
        Card(
            DivVStacked(
                H3(post["title"], cls=TextPresets.bold_lg),
                P(post["date"], cls=TextPresets.muted_sm),
                P(post["summary"], cls=TextPresets.muted_sm),
                # Updated tags section with smaller, more compact styling
                DivLAligned(
                    *[P(tag.replace("-", " "), 
                        cls=TextT.xs + TextT.muted + " bg-gray-50 px-1.5 rounded mr-1") 
                      for tag in post["tags"]],
                    cls="flex-wrap mt-2"
                ),
                cls="h-full"  # Make the inner content container full height; makes all the cards the same height
            ),
            cls="hover:shadow-lg transition-shadow duration-200 h-full"  # Make card full height
        ),
        href=f"/post/{post['slug']}", 
    )

def TagButton(tag, is_selected=False, cls=""):
    """Creates a clickable tag button with selected state"""
    base_cls = "px-3 py-1 rounded-full text-sm transition-colors duration-200"
    selected_cls = "bg-gray-800 text-white" if is_selected else "bg-gray-200 hover:bg-gray-300 text-gray-700"
    return A(
        tag.replace("-", " "),
        href=f"/?tag={tag}" if not is_selected else "/",
        cls=f"{base_cls} {selected_cls} {cls}"
    )

def execute_code_block(code: str):
    """Execute a code block and return its output"""
    # Create a local namespace
    namespace = {}
    
    # Check if the code includes FastHTML/MonsterUI imports
    has_fasthtml = "from fasthtml.common import" in code
    has_monsterui = "from monsterui.all import" in code
    
    # Add default imports only if they're not already present
    default_imports = []
    if not has_fasthtml:
        default_imports.append("from fasthtml.common import *")
    if not has_monsterui:
        default_imports.append("from monsterui.all import *")
    
    # Execute any default imports
    if default_imports:
        exec("\n".join(default_imports), namespace)
    
    # Execute the code and look for _result
    exec(code, namespace)
    if '_result' in namespace:
        return to_xml(namespace['_result'])
    return ''  # Return empty string if no result to show

def format_code_for_display(code: str, show_result_call: bool = False) -> str:
    """Format a code block for display
    
    Args:
        code: The code block to format
        show_result_call: If True, preserve the _result line but strip the '_result = ' prefix
    """
    lines = code.split('\n')
    # Find the last non-empty line
    last_line = next((line for line in reversed(lines) if line.strip()), '')
    
    # If the last non-empty line is a _result assignment
    if '_result =' in last_line:
        # Find the index of the last line
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() == last_line.strip():
                if show_result_call:
                    # Replace '_result = ' with nothing and keep the line
                    lines[i] = lines[i].replace('_result =', '').strip()
                    return '\n'.join(lines)
                else:
                    # Remove the line entirely
                    return '\n'.join(lines[:i])
    
    return '\n'.join(lines)

def process_markdown_content(content: str):
    """Process markdown content and execute special code blocks"""
    parts = content.split("```")
    processed_parts = []
    
    for i, part in enumerate(parts):
        if i % 2 == 0:  # Not a code block
            # Convert markdown to HTML
            html = str(render_md(part))
            
            # Parse HTML and modify links to open in new tabs
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a'):
                # Skip internal links (those starting with /)
                if not link.get('href', '').startswith('/'):
                    link['target'] = '_blank'
                    link['rel'] = 'noopener noreferrer'
            
            processed_parts.append(str(soup))
        else:  # Code block
            if part.startswith('python:show:run') or part.startswith('python:show:run:call'):
                # Get the code without the marker
                show_call = ':call' in part.split('\n')[0]
                code = part[part.index('\n')+1:]
                try:
                    # First show the code
                    display_code = format_code_for_display(code, show_result_call=show_call)
                    processed_parts.append(f'<pre><code class="language-python">{display_code}</code></pre>')
                    # Add vertical spacing
                    processed_parts.append('<div class="my-4"></div>')
                    # Then execute and show the result
                    result = execute_code_block(code)
                    processed_parts.append(str(result))
                    # Add label indicating dynamic content
                    processed_parts.append('<div class="text-gray-400 text-sm mt-2 italic">↑ Live rendered output</div>')
                    # Add spacing after the rendered output
                    processed_parts.append('<div class="mb-8"></div>')
                except Exception as e:
                    processed_parts.append(f'<pre class="error">Error executing code: {str(e)}</pre>')
            elif part.startswith('python:run\n'):
                # Execute the code block
                code = part[len('python:run\n'):]
                try:
                    result = execute_code_block(code)
                    processed_parts.append(str(result))
                    # Add label indicating dynamic content
                    processed_parts.append('<div class="text-gray-400 text-sm mt-2 italic">↑ Live rendered output</div>')
                    # Add spacing after the rendered output
                    processed_parts.append('<div class="mb-8"></div>')
                except Exception as e:
                    processed_parts.append(f'<pre class="error">Error executing code: {str(e)}</pre>')
            else:
                # Regular code block, wrap in pre/code tags
                lang = part.split('\n', 1)[0]
                code = part[len(lang)+1:] if lang else part
                processed_parts.append(f'<pre><code class="language-{lang}">{code}</code></pre>')
                # Add vertical spacing
                processed_parts.append('<div class="my-4"></div>')
    
    return ''.join(processed_parts)

@rt("/")
def get(tag: str = None):
    # Load posts on each request
    posts = load_posts()
    
    # Filter posts if tag is provided
    filtered_posts = [post for post in posts if not tag or tag in post["tags"]]
    
    # Get tag frequencies and sort by most common, then alphabetically for ties
    tag_freq = {}
    for post in posts:  # Use posts instead of blog_posts
        for t in post["tags"]:
            tag_freq[t] = tag_freq.get(t, 0) + 1
    
    # Get top 5 tags sorted by frequency (and alphabetically for ties)
    top_tags = sorted(tag_freq.items(), key=lambda x: (-x[1], x[0]))[:5]
    top_tags = [t[0] for t in top_tags]
    
    return Title("Drew Echerd's Blog"), Container(
        # Header section
        DivVStacked(
            A(H1("Drew Echerd's Blog", cls="mt-8"), href="/"),
            P("Sharing what I'm learning, teaching, and exploring in technology.", 
              cls=TextPresets.muted_lg),
            # Social links
            DivLAligned(
                SocialLink("github", "GitHub", "https://github.com/decherd"),
                SocialLink("twitter", "X.com", "https://twitter.com/drewecherd"),
                cls="space-x-6 mt-4"
            ),
            Divider(cls="my-8")
        ),
        # Blog posts section
        DivVStacked(
            H3("Latest Posts"),
            # Top 5 tags filter
            DivLAligned(
                *[TagButton(t, is_selected=(t == tag), cls="mr-2 mb-2") for t in top_tags],
                cls="flex-wrap"
            ),
            Grid(
                *[BlogPostCard(post) for post in filtered_posts],
                cols_sm=1,
                cols_md=1,
                cols_lg=1,
                cols_xl=1,
                cols_2xl=1,
                gap=6
            )
        ),
        cls="max-w-4xl mx-auto px-4 py-8"
    )

@rt("/post/{post_slug}")
def get(post_slug: str):
    # Load posts on each request
    posts = load_posts()
    
    # Find the post or return 404
    post = next((p for p in posts if p["slug"] == post_slug), None)  # Use posts instead of blog_posts
    if not post:
        return Title("404 - Aw, man!"), Container(
            H1("404 - Aw, man!", cls="text-4xl font-bold mt-8"),
            P("The post you're looking for doesn't exist but I bet it would have been a good one.", cls=TextPresets.muted_lg),
            A("← Back to Home", href="/", cls="text-black hover:text-gray-600 mt-4")
        )
    
    # Process the content and get HTML
    processed_content = process_markdown_content(post["content"])
    
    return Title(f"{post['title']} - Drew Echerd's Blog"), Container(
        DivVStacked(
            # Back link
            A("← Back to Home", 
              href="/", 
              cls="hover:text-gray-600 mb-8"),
            # Post header
            H1(post["title"]),
            P(post["date"], cls=TextPresets.muted_lg + " mt-2"),
            Divider(cls="my-8"),
            cls="w-full"  # Ensure inner content respects container width
        ),
            # Post content with executed code blocks
            Article(
                NotStr(processed_content),
            ),
        cls="max-w-4xl mx-auto px-4 py-8"  # Added w-full
    )

serve()