<p align="center">
 <a href="#-about-the-project">About</a> •
 <a href="#-features">Features</a> •
 <a href="#-layout">Layout</a> • 
 <a href="#-how-to-run-the-project">How to Run</a> • 
 <a href="#-technologies">Technologies</a> • 
 <a href="#-how-to-contribute-to-the-project">Contribute</a> • 
 <a href="#user-content--license">License</a> • 
 <a href="#-contributors">Contributors</a>
</p>

## 💻 About the project

The Lorem Ipsum Generator is a Python library that allows you to generate Lorem Ipsum text easily. Lorem Ipsum is placeholder text commonly used in the printing and typesetting industry.

## ⚙️ Features

- **Lorem Ipsum Paragraphs:** Generate Lorem Ipsum paragraphs effortlessly with the `paragraphs` method.

- **Random Words Generation:** Create a string of random words using the `words` method, allowing customization of the number of words.

- **Shopping List Generation:** Quickly generate a shopping list with randomly selected items using the `shopping_list` method.

---

## 🎨 Layout

---

## 🚀 How to run the project

### Installation

To use the Lorem Ipsum Generator, you first need to install it. You can install it using pip:

```bash
pip install lorem-ipsum-generator
```

### Usage

Import the `LoremIpsum` class and create an instance:

```python
from lorem_ipsum_generator import LoremIpsum

Lorem = LoremIpsum()
```

#### Generating Paragraphs

To generate Lorem Ipsum paragraphs, use the `paragraphs` method:

```python
lorem_paragraphs = Lorem.paragraphs(paragraphs_numbers=3, start_with_lorem_ipsum=True)
print(lorem_paragraphs)
```

This will generate three Lorem Ipsum paragraphs, starting with the default "Lorem ipsum" text.

#### Generating Words

To generate a string of random words, use the `words` method:

```python
lorem_words = Lorem.words(words_numbers=50)
print(lorem_words)
```

This will generate a string containing 50 random words.

#### Generating a Shopping List

To generate a shopping list of randomly selected items, use the `shopping_list` method:

```python
shopping_list = Lorem.shopping_list(items_count=5)
print(shopping_list)
```

This will generate a shopping list with 5 randomly selected items.

### Examples

Here are some additional examples:

```python
# Example 1: Generating 2 paragraphs without starting with "Lorem ipsum"
lorem_text = Lorem.paragraphs(paragraphs_numbers=2, start_with_lorem_ipsum=False)

# Example 2: Generating a string of 20 random words
random_words = Lorem.words(words_numbers=20)

# Example 3: Generating a shopping list with 3 items
shopping_items = Lorem.shopping_list(items_count=3)
```

Feel free to customize the parameters based on your needs.

---

## 🛠 Technologies

---

## Contribution ✨

Help the community make this project even more amazing. Read how to contribute by clicking **[here](https://github.com/oVitorio/.github/blob/main/CONTRIBUTING.md)**. I am convinced that together we will achieve incredible things!

---

## 📝 License

This project is under the license [GLP3 - License](./LICENSE).

---

## 👨‍💻 Contributors

💜 A big thanks 👏 to these folks who brought this project from the realm of ideas to execution!

<table>
  <tr>
    <td align="center"><a href="https://github.com/oVitorio"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/88901960?v=4" width="100px;" alt=""/><br /><sub><b>Vitório Cavaleheiro</b></sub></a><br /><a href="https://github.com/oVitorio" title="github-oVitorio">👨‍🚀</a>
    </td> 
  </tr>
</table>

---
