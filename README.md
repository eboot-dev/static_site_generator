# static_site_generator
Static Webpage Generator written in Python. Boot.dev project

## Architecture

High-level architecture for our static site generator (**SSG**).

- `static/`: static assets likeimages and CSS
- `src/`: Python code, the generator itself. Creats stuffs on the `public/` directory. 
- `src/content/` & `src/template.html`: markdown and HTML template files used by the generator code.
- `public/`: the generator output directory with the filanl HTML and CSS fiels

The flow of data through the full system is:

1. Markdown files are in the `/content` directory. A `template.html` file is in the root of the project.
2. The static site generator (the Python code in `src/`) reads the Markdown files and the template file.
3. The generator converts the Markdown files to a final HTML file for each page and writes them to the `/public` directory.

## Usage
To run the static site generator inside the project's root directory run:
```console
$ ./main.sh
```

## Testing

### Run Unit Tests
To run the unit tests inside the project's root directory run:
```console
$ ./test.sh
```

### Test generated page
To test the generated page:

1. Inside the `public/` directory start the built-in Python HTTP server (e.g. `python3.10 -m http.server 8888`) to serve the contents of the `/public` directory on [http://localhost:8888](http://localhost:8888) (the local machine). 
2. Open a browser and navigate to [http://localhost:8888](http://localhost:8888) to view the rendered site.

## How the SSG Works
The vast majority of our coding happens in the `src/` directory because almost all of the work is done in steps 2 and 3 above. Here's a rough outline of what the final program does when it runs:

1. **Delete** everything in the `/public` directory.
2. **Copy** any static assets (HTML template, images, CSS, etc.) to the `/public` directory.
3. **Generate** an HTML file for each Markdown file in the `/content` directory. 

**For each Markdown file:**
1. **Open** the file and **read** its contents.
2. **Split** the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
3. **Convert** each block into a tree of `HTMLNode` objects. For inline elements (like bold text, links, etc.) convert:
	- Raw markdown -> `TextNode` -> `HTMLNode`
4. **Join** all the `HTMLNode` blocks under one large parent `HTMLNode` for the pages.
5. Use a recursive **`to_html()`** method to convert the `HTMLNode` and all its nested nodes to a giant HTML string and inject it in the HTML template.
6. **Write** the full HTML string to a file for that page in the `/public` directory.

