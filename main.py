from fasthtml.common import *
from monsterui.all import *
from fh_posts.all import *


app, rt = fast_app(
    hdrs=(
        Theme.zinc.headers(mode='light'), 
        HighlightJS(langs=["python", "bash", "yaml", "json"], light="atom-one-dark"),
        Link(rel="icon", type="image/x-icon", href="/images/favicon.ico"),
        Link(rel="mask-icon", type="image/png", href="/images/apple-touch-icon.png")
    ),
    static_path="static",
    live=True
)


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
                H3(post.title, cls=TextPresets.bold_lg),
                P(post.date, cls=TextPresets.muted_sm),
                P(post.summary, cls=TextPresets.muted_sm),
                # Updated tags section with smaller, more compact styling
                DivLAligned(
                    *[P(tag.replace("-", " "), 
                        cls=TextT.xs + TextT.muted + " bg-gray-50 px-1.5 rounded mr-1") 
                      for tag in post.tags],
                    cls="flex-wrap mt-2"
                ),
                cls="h-full"  # Make the inner content container full height; makes all the cards the same height
            ),
            cls="hover:shadow-lg transition-shadow duration-200 h-full"  # Make card full height
        ),
        href=f"/post/{post.slug}", 
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

@rt("/")
def get(tag: str = None):
    # Load posts on each request
    posts = load_posts('posts')
    
    # Filter posts if tag is provided
    filtered_posts = [post for post in posts if not tag or tag in post.tags]
    
    # Get tag frequencies and sort by most common, then alphabetically for ties
    tag_freq = {}
    for post in posts:  # Use posts instead of blog_posts
        for t in post.tags:
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
    posts = load_posts('posts')
    
    # Find the post or return 404
    post = next((p for p in posts if p.slug == post_slug), None)  # Use posts instead of blog_posts
    if not post:
        return Title("404 - Aw, man!"), Container(
            H1("404 - Aw, man!", cls="text-4xl font-bold mt-8"),
            P("The post you're looking for doesn't exist but I bet it would have been a good one.", cls=TextPresets.muted_lg),
            A("← Back to Home", href="/", cls="text-black hover:text-gray-600 mt-4")
        )
    
    # Process the content and get HTML
    rendered_content = post.render(open_links_new_window=True)
    
    return Title(f"{post.title} - Drew Echerd's Blog"), Container(
        DivVStacked(
            # Back link
            A("← Back to Home", 
              href="/", 
              cls="hover:text-gray-600 mb-8"),
            # Post header
            H1(post.title),
            P(post.date, cls=TextPresets.muted_lg + " mt-2"),
            Divider(cls="my-8"),
            cls="w-full"  # Ensure inner content respects container width
        ),
            # Post content with executed code blocks
            Article(rendered_content),
        cls="max-w-4xl mx-auto px-4 py-8"  # Added w-full
    )

serve()