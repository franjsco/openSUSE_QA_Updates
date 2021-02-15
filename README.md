<h1 align="center">osqu</h1>
<p>
  </a>
  <a href="https://twitter.com/franjsco" target="_blank">
    <img alt="Twitter: franjsco" src="https://img.shields.io/twitter/follow/franjsco.svg?style=social" />
  </a>
</p>


> A command-line interface tool to view the latest builds of openSUSE Tumbleweed from openQA

Data: https://openqa.opensuse.org/

<a href="https://asciinema.org/a/391337" target="_blank"><img src="https://asciinema.org/a/391337.svg" /></a>


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/franjsco/osqu ~/.osqu

    cd ~/.osqu
    ```

2. Install dependencies:
    ```sh
    pip3 install -r requirements.txt
    ```

3. Make the script executable:
    ```sh
    chmod +x osqu.py
    ```

4. Create a symbolic link:
    ```sh
    cd /usr/local/bin
    sudo ln -s ~/.osqu/osqu.py osqu
    ```


## Use
Open the terminal and launch:
```sh
osqu
```
