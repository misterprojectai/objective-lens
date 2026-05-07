# GitBook Documentation | Blocks

Add and edit blocks within your content

GitBook is a block-based editor, meaning you can add different kinds of blocks to your content — from standard text and images to interactive blocks. Your pages can include any combination of blocks you want, and there’s no limit to the number of blocks you can have on a page.

### Full-width blocks

By making your blocks full width, you can create a clear visual hierarchy in your content, or simply give more space to content that needs it.

 This feature is available for the following block types:
- Code
- Images
- Tables
- Cards
- Columns
- Integration blocks 

Some blocks will always display full-width, regardless of the page’s width setting in the **Page options** menu:
- OpenAPI

===

# Paragraphs

Add a paragraph block to insert formatted text, inline images and more

A paragraph is the most basic content block you can use on GitBook.

> You can add other inline content to your paragraph, such as emojis, images and Math & TeX.
> You can also format your text using the context menu or keyboard shortcuts, or using Markdown.

## Representation in Markdown

Because a paragraph block is just text, that’s how it’s represented in Markdown.

```
Professionally printed material in English typically does not indent the first paragraph, but indents those that follow. For example, Robert Bringhurst states that we should “set opening paragraphs flush left.”
```

===

# Headings 

Add heading blocks to a page to organize your content and improve SEO

Headings help give your documents structure — and using keywords in headings will also help search engines understand that structure, which can help your page rank higher in search results.

GitBook offers three levels of headings. Heading levels 1 (H1) and 2 (H2) will appear in the page outline.

## Anchor links

When you add a heading to a page, it creates an anchor link. You can then link directly to these specific sections, to point people to relevant information.

#### Link to an anchor

You can see anchor links in public content, or private content in read-only mode, by hovering over the title and clicking the that appears next to it. This will update the URL in your browser’s top bar, so you can copy it to use elsewhere.

If you want to link to a particular anchor from a page within your GitBook space, you can use a relative link, which will update if you change the heading to prevent the link from breaking.

#### Edit an anchor

By default, the anchor link will be identical to the text in your header. If you plan to link to that URL outside of GitBook, changing the header in future will break the anchor link. The link will then take visitors to the top of the page, rather than the anchor location.

To avoid this, you can manually set the anchor link by opening the **Options menu** for the header, then choosing **Edit anchor**. You can then enter the anchor link you wish to use — this will remain the anchor even if you change the header itself.

## Representation in Markdown

GitBook generates SEO optimized pages, meaning page titles in GitBook are automatically represented in markdown as a first level heading:

```
# I'm a page title
```

This means that if you sync your content with Git, page headers added through the editor will be represented as one level lower:

```
## My heading 1
### My heading 2
#### My heading 3
```

===

# Unordered lists 

Add an unordered list block to create bullet point lists

Unordered lists are great for making a series of points that do not necessarily need to be made in a particular order. They are effectively bullet point lists, with support for nesting as needed.

## Representation in Markdown

```
- Item
   - Nested item
      - Another nested item
   - Yet another nested item
- Another item
- Yet another item
```

===

# Ordered lists

Add an ordered or numbered list to a page

Ordered lists, also called numbered lists, help you prioritize items or create a list of steps.

## Representation in Markdown

```
1. Item 1
   1. Nested item 1.1
      1. Nested item 1.1.1
   2. Nested item 1.2
2. Item 2
3. Item 3
```

### Adding an inline image to an ordered list

Adding images inside of ordered lists is possible in GitBook

===

# Task lists

Add a task list to display tasks that can be completed

Task lists allow you to create a list of items with checkboxes that you can check or uncheck.

> **Note:** Readers of your published space will not be able to check or uncheck these boxes. You can decide which boxes are checked and unchecked when you create the content.

## Representation in markdown

```
- [ ] Here’s a task that hasn’t been done
  - [x] Here’s a subtask that has been done, indented using `tab`
  - [ ] Here’s a subtask that hasn’t been done.
- [ ] Finally, an item, unidented using `shift` + `tab`.
```

===

# Hints

Add a hint to a page to draw your reader’s attention to specific pieces of important information.

Hints, or callouts, are a great way to bring the reader’s attention to specific elements in your documentation, such as tips, warnings, and other important information.

There are four different hint styles. Each style uses a default icon, but you can customize the icon by clicking on it and choosing another one from our icons set.

Hint blocks support inline content and formatting, as well some specific block types.

## Representation in Markdown

```
{% hint style="info" %}
**Info hints** are great for showing general information, or providing tips and tricks.
{% endhint %}

{% hint style="success" %}
**Success hints** are good for showing positive actions or achievements.
{% endhint %}

{% hint style="warning" %}
**Warning hints** are good for showing important information or non-critical warnings.
{% endhint %}

{% hint style="danger" %}
**Danger hints** are good for highlighting destructive actions or raising attention to critical information.
{% endhint %}

{% hint style="info" %}

{% hint style="info" icon="books" %}
This hint block has a custom icon.
{% endhint %}

## This is a H2 heading

This is a line

This is an inline <img src="../../.gitbook/assets/25_01_10_command_icon_light.svg" alt="The Apple computer command icon" data-size="line"> image

- This is a second <mark style="color:orange;background-color:purple;">line using an unordered list and color</mark>
{% endhint %}
```

===

# Quotes

Add a quote block to a page to highlight copy you’re adding from elsewhere, or to draw attention to a specific part of your text

Quotes are useful when you want to include something from another source.

## Representation in Markdown

```
> "No human ever steps in the same river twice, for it’s not the same river and they are not the same human." — _Heraclitus_
```

===

# Code blocks

Add a code block to a page to include sample code, configurations, code snippets and more

You can add code to your GitBook pages using code blocks.

When you add a code block, you can choose to set the syntax, show line numbers, show a caption, and wrap the lines.

A code block may be useful for:
-   Sharing configurations
-   Adding code snippets
-   Sharing code files
-   Showing usage examples of command line utilities
-   Showing how to call API endpoints
-   And much more!

### Example of a code block

> You can also combine code blocks with a tabs block to offer the same code example in multiple different languages:

> You can make code blocks span the full width of your window next to the block and choosing **Full width**.

### Code block options

#### Set syntax…

You can set the syntax in your code block to any of the supported languages. This will enable syntax highlighting in that language, too.

#### With line numbers

This will toggle line numbers for your code on and off.

Showing line numbers is useful when the code represents the contents of a file as a whole, or when you have long code blocks with lots of lines. Hiding line numbers is useful for snippets, usage instructions for command line or terminal expressions and similar scenarios.

#### With caption

This will toggle a caption that sits at the top of the block, above your lines of code.

The caption is often the name of a file, but you can also use it as a title, description, or anything else you’d like.

#### Wrap code

This will toggle code wrapping on and off, so long lines of code will wrap to all be visible on the page at once.

Wrapping lines is useful when your code is long and you want to avoid having the viewer scroll back and forth to read it. If you toggle **Wrap code** on, you may also want to show line numbers — this will make it easier to read the code and understand where new lines start.

#### Expandable

This will toggle showing the code in full (when the toggle is off) or a collapsed window of the code which the user can expand (when the toggle is on).

The collapsed view defaults to showing 10 lines of code with an button to expand to show the full code block. If there are less than 10 lines of code, all the content will be shown.

### Code block actions

As well as the options above, you can also change the language the code block displays, and copy your code instantly.

#### Copy the code

Hover over a code block and a number of icons will appear. Click the middle icon to copy the contents of the code block to your clipboard.

## Representation in Markdown

<markdown>
{% code title="index.js" overflow="wrap" lineNumbers="true" %}

```javascript
‌import * as React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(<App />, window.document.getElementById('root'));
```

{% endcode %}
</markdown>

===

# Files

Manage and add files to your space such as PDFs, videos, documents and more

You can upload files to your GitBook space and add them to your page for people to view or download.

You can show some files, such as images and OpenAPI files, on the page itself for people to see without clicking anything. For others, such as PDFs, users will have to click to view or download it.

You can also optionally add a caption below any file you insert into your page to add more information if needed.

### Uploading a file

You can manage uploaded files in the Files side panel of your space. You can find the Files panel at the top of your space’s table of contents.

To upload a file, drag and drop it into the **Drop your file or browse** section, or select it and use your system file dialog to select the file you want to upload.

> GitBook allows you to upload files up to 100MB per file.

You can also add files to your space when you add an image block or an OpenAPI block. When you create one of these blocks, the Files panel will open, so you can either select a file, or upload a new file.

### Replacing a file

If you have a file that simply needs updating to a new version, you can replace it. This will swap out the old file and put the new file in its place. Any blocks that previously referred to the old file will then refer to the new file.

To replace a file, open the **Actions menu** for the file and click **Replace**. In the file replacement dialog that appears, select the new file and wait for the upload indicator to complete. Your file will automatically update everywhere it appeared in your space.

This can be helpful if, for example, you’ve had a major product redesign and need to update outdated UI screenshots that appear on multiple pages. Replacing the original file would update the screenshot everywhere in your space, saving you time and effort.

> **Tip:** Once you’ve uploaded an image or a file, you can reference it anywhere in your space by creating an image or a file block and selecting it from the **Files** side panel.
> We recommend you do this rather than uploading the image again every time you want to include it, to make it easier to replace images later and to avoid having multiple files with the same name.

## Representation in Markdown

```
{% file src="https://example.com/example.pdf" %}
    This is a caption for the example file.
{% endfile %}
```

===

# Images

Add an image or a gallery of images to a page, add image variants for dark mode, and resize and align images to your needs

You can insert images into your page, then choose their size and whether to align them to the left, center, or right. You can also optionally include alt text and/or a caption on your image block.

> **Tip:** For accessibility purposes, we recommend setting alt text for your images.

### Create an image gallery

Adding more than one image to an image block will create a gallery.

### Adding images for light & dark mode

You can set different images for the light and dark mode versions of your published site. GitBook will automatically display the correct image depending on the mode your visitor is in.

> **Note:** GitBook doesn’t currently support light and dark mode images for certain cases, including page covers or image covers on cards.

### Light and dark mode images through GitHub/GitLab Sync

You can also add light and dark mode images in Markdown through HTML syntax (`<picture>` and `<source>`).

For block images, use the `<figure>` HTML element with a `<picture>` and `<source>` in it:

```
Text before

<figure>
  <picture>
    <source
      srcset="
        https://user-images.githubusercontent.com/3369400/139447912-e0f43f33-6d9f-45f8-be46-2df5bbc91289.png
      "
      media="(prefers-color-scheme: dark)"
    />
    <img
      src="https://user-images.githubusercontent.com/3369400/139448065-39a229ba-4b06-434b-bc67-616e2ed80c8f.png"
      alt="GitHub logo"
    />
  </picture>
  <figcaption>Caption text</figcaption>
</figure>

Text after
```

For inline images (images that sit inline with text), use the `<picture>` HTML element with a `<source>` in it:

Copy

```
Text before the image
<picture
  ><source
    srcset="
      https://user-images.githubusercontent.com/3369400/139447912-e0f43f33-6d9f-45f8-be46-2df5bbc91289.png
    "
    media="(prefers-color-scheme: dark)" />
  <img
    src="https://user-images.githubusercontent.com/3369400/139448065-39a229ba-4b06-434b-bc67-616e2ed80c8f.png"
    alt="The GitHub Logo"
/></picture>
and text after the image
```

> **Note:** We don’t yet support GitHub-only syntax through `#gh-dark-mode-only` or `#gh-light-mode-only`.

### Resizing

Resize an image
-   **Small** – 25% of the image size
-   **Medium** – 50% of the image size
-   **Large** – 75% of the image size
-   **Fit** – Removes all size specifications and displays either at full size or capped at a maximum width of **735** **pixels** for larger images.
    

If your image is wider than the editor, GitBook will limit the image’s width to the editor’s width instead, and resizing will be based on this limit.

>**Note:** When resizing images in an image gallery, the results can differ from resizing an individual image.

> You can make image blocks span the full width of your window.

### Resizing images through Git Sync

If you want more control over the sizing of your image, you can specify the exact size using Markdown in GitHub or GitLab.

When we export an image, we use the HTML tag `<img/>`. As per the specifications, we can specify the dimensions of the image using the `width` and `height` attributes, which only accept values in pixels or a combination of a number and a `%` sign. 

Valid variants for specifying the image dimensions are:
* `<img width="100" />` Sets the image to 100 pixels wide
* `<img width="100%" />` Sets the image to full size (although this will be limited by the editor)

### Aligning images

By default, image blocks will show your image at its full size, aligned centrally. This will only affect images that are narrower than the editor, or images you’ve resized.

### Framing images

You can add a frame to image blocks to give your images a consistent look and visually separate them from their surrounding content.

Framed images can have captions, and show a subtle grid behind the caption.

> **Good to know:** You can only frame single images in a block. Image blocks that contain multiple images and inline images cannot have frames.

## Representation in Markdown

```
//Simple Block
![](https://gitbook.com/images/gitbook.png)

//Block with Caption
![The GitBook Logo](https://gitbook.com/images/gitbook.png)

//Block with Alt text

<figure><img src="https://gitbook.com/images/gitbook.png" alt="The GitBook Logo"></figure>

//Block with Caption and Alt text

<figure><img src="https://gitbook.com/images/gitbook.png" alt="The GitBook Logo"><figcaption><p>GitBook Logo</p></figcaption></figure>

// Block with framed image

<div data-with-frame="true"><img src="https://gitbook.com/images/gitbook.png" alt="The GitBook Logo"></div>

//Block with different image for dark and light mode, with caption

<figure>
  <picture>
    <source srcset="https://user-images.githubusercontent.com/3369400/139447912-e0f43f33-6d9f-45f8-be46-2df5bbc91289.png" media="(prefers-color-scheme: dark)">
    <img src="https://user-images.githubusercontent.com/3369400/139448065-39a229ba-4b06-434b-bc67-616e2ed80c8f.png" alt="GitHub logo">
  </picture>
  <figcaption>Caption text</figcaption>
</figure>
```

===

# Embedded URLs

Embed videos, music and more directly into your page with a URL

> **Note:** The content you want to embed must be publicly available in order for GitBook to access the file. For example, when embedding a Google doc the share settings must be set to _Anyone with the link_.

### Videos

> **Note:** You can choose to auto-play and loop YouTube and Vimeo embeds by adding `?autoplay=1&loop=1` to the end of your video’s URL.

## Representation in Markdown

```
{% embed url="URL_HERE" %}
```

===

# Tables

Keep information organized and make documenting data easier with tables

You can add tables to better organize your information in a GitBook page.

### Table block options

You’ll have a number of options to change the appearance and manage the data inside the table:
- **Table/Cards:** Choose to display your data as either a table block or [a cards block](/docs/creating-content/blocks/cards). GitBook populates both these blocks using the same data, so you can switch between them depending on the look and design you want.
- **Add column:** Add a new column to the right of your table. You can choose column type using the menu, or just click **Add column** to add a text column.
- **Insert row:** Add a new row to the bottom of your table.
- **Show header:** Hide or show the top title row of your table.
- **Freeze header:** Keep the top row of your table visible on the page while you scroll through the rows below. This is useful for larger tables where you want the column titles to stay in view.
- **Freeze first column:** Keep the leftmost column of your table visible while horizontally scrolling through the columns to the right. This is useful for wider tables that overflow the page width, where you want the row labels or identifiers to stay in view.
- **Reset column sizing:** If you’ve changed the column widths, this will reset them all to be equal again.
- **Visible columns:** Choose which columns are visible and which are hidden. If you have hidden columns in your table, this menu is where you can make them visible again.
- **Full width:** Make your table span the full width of your window. This is great for tables with lots of columns.
- **Delete:** Deletes the table block and all of it’s content.
    

### Changing a column type

Depending on the data you want to display, you can set table columns can have different data types. These add formatting, embellishments or restrictions to every cell in the column:
- **Text:** A standard text column, with standard formatting support.
- **Number:** A number column, with or without floating digits.
- **Checkbox:** A checkbox on each line that can be checked or unchecked.
- **Select:** You can select data from a list of options that you can define by opening the **Columns options** menu and choosing **Manage options**. This can be single-choice or multiple-choice.
- **Users:** You can add the name and avatar of a member of your organization. This can be single-choice or multiple-choice.
- **Files:** You can reference a file in the space. You can upload new files when populating cells in the column.
- **Rating:** A star rating. You can configure the maximum rating by opening the **Column options** menu and choosing **Max**.

Use the **Column options** menu to change a column’s type. When you change a column type, you’ll see a prompt asking you to confirm the change, as column data could be deleted or broken by this action.

### Resizing columns

A pixel count appears above the cursor to help you set consistent column sizes.

GitBook stores column sizes as a percentage of the overall width, which allows for relative sizing based on the overall width of the table.

### Scrolling tables

Tables that are wider than the editor container will be horizontally scrollable.

### Images in tables

When you click into a table cell, you can hit the / key to insert images. Images cannot be added to the header row of a table.

## Representation in Markdown

```
# Table

|   |   |   |
| - | - | - |
|   |   |   |
|   |   |   |
|   |   |   |
```

## Can I create nested tables in GitBook?

It's not possible to nest tables in GitBook. To ensure documents remain easy to write, reliable to render, and accessible for all users, GitBook keeps tables flat.

Once a table sits inside another table cell, it becomes difficult to edit, resize, navigate, or maintain consistent formatting across devices.

Nested tables also introduce significant complexity in the underlying document structure, often breaking clean semantics and leading to unpredictability in features such as Git Sync.

===

# Cards

Display information more dynamically with a set of cards — with or without images

You can use cards to create a visually pleasing page layout, combining text and images in a grid. They’re ideal for building landing pages or displaying any other content in a non-linear way.

You can adjust switch between medium or large cards) and link them to the relevant resources.

### Adding links

Here you can add a target link, so users can jump directly to a location when they click the card.

> When creating cards, we recommend you use **target links instead of hyperlinks**. With a target link, your readers can click anywhere on the card to access the linked URL.

### Adding images

Here you can add a cover image to your card. Alternatively, just click the **Add cover image** option on the card itself.

#### Adding images for dark mode

You can also add cover images that will only show in dark mode.

#### Choosing the right image size

GitBook will automatically crop landscape images to a 16:9 ratio on desktop and mobile. If the images you upload are portrait or have a 1:1 ratio, they will be cropped to 16:9 on desktop and display as square or portrait on mobile.

On desktop, all card images will display in a landscape 16:9 ratio, regardless of their dimensions. We recommend using the same dimensions for consistency.

On mobile, square or portrait images will displayed as shown on the left. Landscape images will be displayed as shown on the right.

To keep things consistent across desktop and mobile, we recommend uploading all the images for your cards in a 16:9 format (e.g. 1920px x 1080px).

If you want your cards to adapt their layout depending on the screen size, we’d recommend uploading images with a 1:1 ratio, and the content of your image centered.

### Changing the size of cards

> You can make card blocks span the full width of your window.

## Representation in Markdown

```
<table data-view="cards">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th data-hidden data-card-target data-type="content-ref"></th>
      <th data-hidden data-card-cover data-type="files"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Example title 1</strong></td>
      <td>Example description 1.</td>
      <td><a href="https://example.com">https://example.com</a></td>
      <td><a href="https://example.com/image1.svg">example_image1.svg</a></td>
    </tr>
    <tr>
      <td><strong>Example title 2</strong></td>
      <td>Example description 2.</td>
      <td><a href="https://example.com">https://example.com</a></td>
      <td><a href="https://example.com/image2.svg">example_image2.svg</a></td>
    </tr>
    <tr>
      <td><strong>Example title 3</strong></td>
      <td>Example description 3.</td>
      <td><a href="https://example.com">https://example.com</a></td>
      <td><a href="https://example.com/image3.svg">example_image3.svg</a></td>
    </tr>
  </tbody>
</table>
```

===

# Tabs

Add tabs so you can display large blocks of related information without creating a long, hard-to-navigate page

A tab block is a single block with the option to add multiple tabs.

Each tab can contain multiple other blocks, of any type. So you can add code blocks, images, integration blocks and more to individual tabs in the same tab block.

## Representation in Markdown

```
{% tabs %}

{% tab title="Windows" %} Here are the instructions for Windows {% endtab %}

{% tab title="OSX" %} Here are the instructions for macOS {% endtab %}

{% tab title="Linux" %} Here are the instructions for Linux {% endtab %}

{% endtabs %}
```


===

# Expandable

Add an expandable block to a page to keep your pages shorter, hide longer content, or create FAQs

Expandable blocks are helpful in condensing what could otherwise be a lengthy paragraph. They are also great in step-by-step guides and FAQs.

By default, expandable blocks will be collapsed on your published docs site.

## Representation in Markdown

```
# Expandable blocks

<details open>

<summary>Add your expandable title here</summary>

Add your expandable body text here. This expandable is expanded by default.

</details>

<details>

<summary>Add your expandable title here</summary>

Add your expandable body text here. This expandable is collapsed by default.

</details>
```

### Limitations

There are some limitations on which blocks you can create inside of an expandable block.

===

# Stepper

Add a step-by-step guide to a page — perfect for guides, walkthroughs and technical troubleshooting processes

Stepper blocks let you break down a tutorial or guide into separate, but clearly linked steps. Each step can contain multiple different blocks, allowing you to add detailed information.

## Representation in Markdown

```
## Example

{% stepper %}
{% step %}
### Step 1 title
Step 1 text
{% endstep %}
{% step %}
### Step 2 title
Step 2 text
{% endstep %}
{% endstepper %}
```

### Limitations

There are some limitations on which blocks you can create inside of a stepper block — for example, you cannot add expandable blocks or another stepper block. 

===

# Updates

Add one or more updates to a page — perfect for adding a changelog to your site

An updates block lets you share new releases on your site in a format that matches established best practices for changelog updates.

You can add a date to your update block, then format the content inside the block using other blocks as you would expect. You can choose between the full date, a shortened date, or a date using only numbers (e.g. 12/25/2025).

Once you’ve added an update block to your page, you can hover your cursor above or below the block to see the option to add another in sequence.

Each update block can also have its own tags. Use the tag picker below the date to add, remove, or reorder tags.

### RSS feeds

Any page containing an updates block automatically gets an RSS feed, making it easy for your readers to stay on top of new updates.

Users can open the RSS feed from the button at the top of the page, copy the URL, and paste it into their preferred reader. Any updates you publish in your changelog will automatically be pushed to that reader so they’ll see them in real-time.

## Representation in Markdown

```
{% updates format="full" %}
{% update date="2025-12-25" tags="beta" %}
## A brand new update

This block is perfect for telling users all about a brand new update to your product. You can easily add other blocks within this update block, including images, code, lists and much more.
{% endupdate %}
{% endupdates %}
```

===

# Math & TeX

Add a mathTeX block to a page when you want to display a mathematical formula in your documentation

You can use the mathTeX format to include mathematical formulae in your documentation.

You can also add mathTeX as inline content.

## Representation in Markdown

f(x)\=x∗e2piiξxf(x) = x \* e^{2 pi i \\xi x}f(x)\=x∗e2piiξx

```
# Math and TeX block

$$f(x) = x * e^{2 pi i \xi x}$$
```

===

# Page links

Add a page link block to show relations between pages in your space.

Page link blocks are the best way create relations between different pages within your content. Page links stand out on the page as they fill their own block — compared to a hyperlink added to some text.

## Representation in Markdown

```
{% content-ref url="./" %} . {% endcontent-ref %}
```

===

# Columns

Add a column to create different layouts in your documentation.

Columns are a great way to create different layouts for your documentation. You can add many different types of blocks inside a column, and adjust the width of each side to customize it to the design you need.

## Representation in Markdown

```
## Example

### Create a seamless experience between your docs and product

Integrate your documentation right into your product experience, or give users a personalized experience that gives them what they need faster.

<a href="https://www.gitbook.com/#alpha-waitlist" class="button primary">Learn more</a>

<figure><img src="../../.gitbook/assets/GitBook vision post.png" alt="An image of GitBook icons demonstrating side by side column functionality"><figcaption></figcaption></figure>

```

===

# Conditional content

Conditional content blocks let you control who can see a given block of content on your page based on user data and variables. These variables can be passed in via cookies, feature flags, authenticated access, or URL parameters.

### Create conditional content

You’ll be able to write your condition as an expression that will run against data defined in your site. You can reference data from variables, or data coming from visitors through their claims.

See adaptive content for more details.

## Representation in Markdown

```
## Example

{% if visitor.claims.unsigned.example_attribute_A %}
This block is only visible to users **with** attribute A.
<a href="https://gitbook.com/docs/creating-content/blocks/conditional-content?visitor.example_attribute_A=false" class="button primary">View without attribute A</a>
{% endif %}

{% if !visitor.claims.unsigned.example_attribute_A %}
This block is only visible to users **without** attribute A.
<a href="https://gitbook.com/docs/creating-content/blocks/conditional-content?visitor.example_attribute_A=true" class="button primary">View with attribute A</a>
{% endif %}
```

===

# Variables and expressions

Create reusable variables that can be referenced in pages and spaces

With variables you can create reusable text that can be conditionally referenced in expressions and conditions for adaptive content.

If you repeat the same name, phrase or version number multiple times within your content, you can create a **variable** to help keep all those instances in sync and accurate — which is useful if you ever need to update them, or they’re complex and often mistyped.

You can create variables that are scoped to a single page, or a single space.

### Create a new variable

You can add variables to a single page or an entire space. When you update the value of a variable, every instance of it will update.

> Variable names must start with a letter, and can contain letters, numbers and underscores.

### Use variables in your content

Variables can be referenced and used within an expression — which you can insert into your content inline.

Variables defined under your page are accessible under the `page.vars` object. Similarly, variables defined across your entire space are accessible under the `space.vars` object.

You can add variables to your content within expresions. The expression editor offers autocomplete options to help you find the variable you need.

### Update a variable

You can update a variable at any point when within a change request. Updating its value will update the value across any expression blocks referencing it. The changed variable will go live to any published site once the change request is merged.
