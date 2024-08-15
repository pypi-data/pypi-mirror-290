<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->

<a name="readme-top"></a>

<div align="center">
  <h1 align="center">Versification Utils</h3>

  <p align="center">
    Tools to detect and convert between Bible versifications
    <br />
    <!-- <a href="https://github.com/jcuenod/versification_utils"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/jcuenod/versification_utils">View Demo</a>
    · -->
    <a href="https://github.com/jcuenod/versification_utils/issues">Report Bug</a>
    ·
    <a href="https://github.com/jcuenod/versification_utils/issues">Request Feature</a>
    <!-- ·
    <a href="https://jcuenod.github.io/versification_utils-examples/">Live Demo</a> -->
  </p>
</div>



<!-- GETTING STARTED -->
## Getting Started

### Installation

To install, use your favorite package manager and do the equivalent of:

```sh
pip install versification-utils
```

<!-- USAGE EXAMPLES -->
### Usage

`versification-utils` provides three main functions: `detect`, `remap_verses`, and `to_vref`.

#### Detecting Versification

The `detect` function analyzes a list of verse references and returns the versification system that best fits the references. The function returns a string with the name of the versification system (or a list of versification schemas, if there was a tie).

```python
from versification_utils import detect

detect(["JHN 3:16", "JHN 3:17", "JHN 3:18"])
# ['eng', 'rsc', 'rso', 'vul', 'org', 'lxx', 'unk']
```

The schemas are abbreviated as follows:
- `eng`: English (Protestant)
- `rsc`: Russian (Synodal)
- `rso`: Russian (Orthodox)
- `vul`: Vulgate
- `org`: Original (Hebrew/Greek)
- `lxx`: Septuagint
- `unk`: Unknown

In this case, the verse references were insufficient to rule out any possibilities. But if we add more references, we can narrow down possibilities:

```python
detect(["PSA 22:31", "PSA 23:6"])
# 'eng'

detect(["PSA 22:32", "PSA 23:6"])
# 'org'
```

Only the `eng` versification system ends Psalms 22 with v. 31 and 23 with v. 6. So the first example returns `'eng'`, while the second example returns `'org'`. Technically, the diagnostics only examine the the last verse number of each chapter right now. This may change in future, so the `detect` function expects a list of USFM verse references. You should just pass in all the references you have (which would make for a convoluted example here).

#### Remapping Verses

If you know the versification schema your references follow, you can use the `remap_verses` function to convert them to another schema. This function takes a dictionary of verses that map the reference to the verse text, and returns a new dictionary with modified (remapped) references.

```python
from versification_utils import remap_verses

verses = {
    "PSA 22:31": "The last verse of Psalm 22",
    "PSA 23:6": "The last verse of Psalm 23"
}

from_schema = "eng"
to_schema = "org"
new_verses = remap_verses(verses, from_schema, to_schema)
# {'PSA 22:32': 'The last verse of Psalm 22', 'PSA 23:6': 'The last verse of Psalm 23'}

from_schema = "eng"
to_schema = "lxx"
new_verses = remap_verses(verses, "eng", "lxx")
# {'PSA 21:32': 'The last verse of Psalm 22', 'PSA 22:6': 'The last verse of Psalm 23'}
```

**Note:** In the second example, the LXX chapters are offset by one.

#### Exporting a Vref File

If you have a dictionary of verses, you can export them to a vref file using the `to_vref` function. This function takes a target `filename`, dictionary of `verses` (like the `remap_verses` function), and the `versification` schema of the verses. If the verses are not in `org` versification, `to_vref` will remap them to `org` before exporting.

```python
from versification_utils import to_vref

verses = {
    "PSA 22:31": "The last verse of Psalm 22",
    "PSA 23:6": "The last verse of Psalm 23"
}

to_vref("eng-my_translation.vref", verses, "eng")
# The vref file "./eng-my_translation.vref" will be created
```



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.md` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/jcuenod/versification_utils.svg?style=for-the-badge
[contributors-url]: https://github.com/jcuenod/versification_utils/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/jcuenod/versification_utils.svg?style=for-the-badge
[forks-url]: https://github.com/jcuenod/versification_utils/network/members
[stars-shield]: https://img.shields.io/github/stars/jcuenod/versification_utils.svg?style=for-the-badge
[stars-url]: https://github.com/jcuenod/versification_utils/stargazers
[issues-shield]: https://img.shields.io/github/issues/jcuenod/versification_utils.svg?style=for-the-badge
[issues-url]: https://github.com/jcuenod/versification_utils/issues
[license-shield]: https://img.shields.io/github/license/jcuenod/versification_utils.svg?style=for-the-badge
[license-url]: https://github.com/jcuenod/versification_utils/blob/master/LICENSE.txt