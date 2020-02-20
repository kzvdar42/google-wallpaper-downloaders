# Google Wallpaper Downloaders

Google provided us with some impressive wallpapers.

* [Chrome OS][Chrome OS link]
* [Google Maps][Maps link] (code exported from 3.0.3 version)

Now you can use them locally!

## Usage

### Chrome OS version

Just use Python 3.4+, no dependencies required.
```
$ python3 chrome-os/download-wallpapers.py
```

Wallpapers will be downloaded to `chrome-os/wallpapers`.
Be wary of download sizes: Chrome OS wallpapers are 200+ MB combined.

### Maps version

For this version you also can use Python 3.4+, but If you don't have `requests` and `tqdm` packages installed, install them using the next command:
```
$ pip install -r requirements.txt
```
`tqdm` package is not required, but if you want a progress bar to show the percentage of the downloads, consider installing it.

To run it:
```
$ python3 maps/download-wallpapers.py
```

Wallpapers will be downloaded to `maps/wallpapers`.
Be wary of download sizes: Maps are 1.8+ GB (up to 3+ GB).

Maps version now can use two different ways to download the image:
* Official links - links used by the plugin when you use the `Download wallpaper` button (with watermarks).
* Internal links - links used by the plugin to show you the image in new tab (without watermarks).

Both of this methods provide you with the 1800x1200 images, but the "Official links" method provide you with watermarked images and no optimization, so images will weight more.

## Code doesn't work?
Check the version of the [Chrome extention][Maps link], if it's bigger than `3.0.3`, then maybe they just updated the API and it's your time to change the code. Look at the code of the extention and extract the links and ids of the images. And don't forget to Pull Request the changes.

[Chrome OS link]: https://chrome.google.com/webstore/detail/chrome-os-wallpapers/dkfibabkihblcenahmcdmfepojcejoan
[Maps link]: https://chrome.google.com/webstore/detail/earth-view-from-google-ma/bhloflhklmhfpedakmangadcdofhnnoh
