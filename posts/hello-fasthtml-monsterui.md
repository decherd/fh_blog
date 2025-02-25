---
title: Hello FastHTML and MonsterUI
summary: An introduction to FastHTML and MonsterUI.
date: February 25, 2025
tags:
  - python
  - fasthtml
  - monsterui
---

[FastHTML](https://fastht.ml), created by [Jeremy Howard](https://x.com/jeremyphoward), and [MonsterUI](https://monsterui.answer.ai) created by [Isaac Flath](https://x.com/isaac_flath), provide a powerful combination for building modern web applications in Python.

## FastHTML

>FastHTML is a general-purpose full-stack web programming system, in the same vein as Django, NextJS, and Ruby on Rails. The vision is to make it the easiest way to create quick prototypes, and also the easiest way to create scalable, powerful, rich applications.

Here is how easy it is to create a 'Hello World' application with FastHTML:
```python
from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app()

@rt("/")
def get():
    return Title("Hello World")
```

## MonsterUI

While FastHTML includes PicoCSS out of the box, it can still be difficult to style your application or create complex designs. This is where MonsterUI comes in.

The best place to learn about MonsterUI is from the post on Answer.AI's blog [MonsterUI: Bringing Beautiful UI to FastHTML](https://www.answer.ai/posts/2025-01-15-monsterui.html). This post is full of examples and explains why MonsterUI is a great choice for building web applications in Python.

MonsterUI sits on top of FastHTML and provides a set of components that make it easier to build modern web applications. It is a component library that is styled with Tailwind CSS and brings FrankenUI, UIKit, DaisyUI, Lucide Icons, and Tailwind UI to Python.

In the same way that with FastHTML you can build a basic web application with just 6 lines of code but extend it to build almost anything, MonsterUI allows you to build beautiful, responsive, and modern web applications with just a few lines of code with default styles or you can extend them with Tailwind CSS in any way you want.

This design principle of making it easy to start but also giving you the flexibility to extend and customize makes both FastHTML and MonsterUI a great choice for building web applications in Python.

Here is an example card from the blog post linked above:
```python:show:run
def TeamCard(name, role, location="Remote"):
    icons = ("mail", "linkedin", "github")
    return Card(
        DivLAligned(
            DiceBearAvatar(name, h=24, w=24),
            Div(H3(name), P(role))),
        footer=DivFullySpaced(
            DivHStacked(UkIcon("map-pin", height=16), P(location)),
            DivHStacked(*(UkIconLink(icon, height=16) for icon in icons))),
            cls="max-w-sm mx-auto"
    )
_result = TeamCard("James Wilson", "Senior Developer", "New York")
```
## Getting help from AI

Both FastHTML and MonsterUI use [llms.txt](https://llmstxt.org), a standard for creating documentation for LLMs so that AI tools can understand how to use these tools. This means that you can use your favorite AI coding helper today with this new library even though the model wasn't trained on the FastHTML or MonsterUI documentation.

For [Cursor](https://www.cursor.com) users you just type `@doc` then choose “Add new doc”, and use this [/llms-ctx.txt](https://docs.fastht.ml/llms-ctx.txt) link. Do the same for MonsterUI with this [/llms-ctx.txt](https://raw.githubusercontent.com/AnswerDotAI/MonsterUI/refs/heads/main/docs/llms-ctx.txt) link.

If you want to know what other sites have their documentation in the llms.txt format, you can see the list on <https://llmstxt.site>.

## You can do anything with code

As I tell the high school students I am teaching a Python Programming class to, "You can do anything with code." The limit has always been with your imagination and the time it takes to build it. With libraries like FastHTML and MonsterUI, the time it takes to build it has never been lower.

## This blog was built in a day with FastHTML and MonsterUI

I'm just getting started myself with FastHTML and MonsterUI, but I've already built this blog with it. As of this publishing, it already has tag filtering and a responsive design. Each blog post is a markdown file that is rendered to HTML. You can check out the source code on [GitHub](https://github.com/decherd/fh_blog).

Check out some of these other blogs built with FastHTML:

- [Isaac Flath's blog](https://isaac.up.railway.app)
- [Marius Vachon's blog](https://blog.mariusvach.com) - I took inspiration from his blog design for this one
- [Simon Moisselin's blog](https://simn.fr)

## Dynamic content and what's next

I don't know if you noticed above but I've added some code blocks that are rendering the output of that code each time this page is loaded. Say 'goodbye' to static blog sites and 'hello' to dynamically rendered content.

If you are intersted in how I built this blog or other things I'm working on, you can follow me on [X](https://x.com/drewecherd) or [GitHub](https://github.com/decherd). My next post will be about how I'm rendering code blocks dynamically.

Thanks for reading and let me know what you think!