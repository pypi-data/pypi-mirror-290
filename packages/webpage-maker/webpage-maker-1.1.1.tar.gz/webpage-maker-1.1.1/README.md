# WebpageMaker

#### Description
It is Python library for generating (rendering) static HTML web pages.

#### What can it do?
It can make lots of webpages and render them for you!

#### How can I use it?
You can import it using the following code:
```python
import wpmaker
```
Then you can use it to create your first HTML webpage created using WebpageMaker!

You can also use the following code to create a new HTML object (which is essentially an instance of a class):
```python
webpage = wpmaker.newHtmlObj(head=wpmaker.title("Hello World"), body=wpmaker.h("Hello, world!"))
```
You can retrieve the generated HTML document at any time through the ```code``` attribute of this instance. For example:
```python
print(webpage.code)
```

And you can find more information in the [official document](https://wpmaker.wcfstudio.cn).