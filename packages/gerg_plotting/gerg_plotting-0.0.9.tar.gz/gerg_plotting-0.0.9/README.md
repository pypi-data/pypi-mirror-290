<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/alecmkrueger/gerg_plotting">
    <img src="https://raw.githubusercontent.com/alecmkrueger/project_images/9af2f8f58c93e183ac5473a4474619407aee08d3/gerg_logo.svg" alt="Logo" width="500" height="272">
  </a>

<h3 align="center">GERG Plotting</h3>

  <p align="center">
    Data plotting package for GERG
    <br />
    <a href="https://github.com/alecmkrueger/gerg_plotting"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/alecmkrueger/gerg_plotting/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/alecmkrueger/gerg_plotting/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#dependencies">Dependencies</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project was created to streamline and standardize the process of generating plots at GERG.



### Built With

[![Python][Python]][Python-url]



<!-- GETTING STARTED -->
## Getting Started

There are three ways to get started
1. Create a fresh virtual environment using your favorite method and install the dependencies
2. Use an already established virtual environment and install the dependencies



### Dependencies
I have provided some commands to install the dependencies using conda but you can use any package manager

List of dependencies:
* python = 3.12
* numpy = 2.0.0
* pandas = 2.2.2
* matplotlib = 3.9.1
* xarray = 2024.6.0
* attrs = 23.2.0
* netcdf4 = 1.7.1.post1
* cmocean = 4.0.3
* scipy = 1.14.0
* mayavi = 4.8.2


### Installation

1. Activate your virtual environment
1. Use pip to install ```pip install gerg_glider```



<!-- USAGE EXAMPLES -->
## Usage

Plot data at GERG using Python.

Create Histgrams for U and V current vectors
```sh
import xarray as xr
import matplotlib.pyplot as plt
from gerg_plotting import Histogram, Buoy

# Open in the dataset
ds = xr.open_dataset('../test_data/buoy.nc')
# Convert the dataset to pandas dataframe
df = ds[['u','v']].to_dataframe().reset_index()

# Initialize the buoy instrument data container
buoy = Buoy(depth=df['bin'].to_numpy(),
            time=df['date'].to_numpy(),
            u_current=df['u'].to_numpy(),
            v_current=df['v'].to_numpy())

# Initialize the figure and axes
fig,axes = plt.subplots(nrows=2,figsize = (5,10))
# Initialize the histogram plotter
hist = Histogram(instrument=buoy)
# Plot the 1-d histograms for u and v currents
hist.plot(fig=fig,ax=axes[0],var='u_current',bins=100)
hist.plot(fig=fig,ax=axes[1],var='v_current',bins=100)
# Add Titles to Histograms
axes[0].set_title('Current Vector U')
axes[1].set_title('Current Vector V')
# Show Figure
plt.show()
```
![ocean current vector histograms ](https://github.com/alecmkrueger/project_images/blob/main/example_u_v_histograms.png?raw=true)




<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request





<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Alec Krueger - alecmkrueger@tamu.edu

Project Link: [https://github.com/alecmkrueger/gerg_plotting](https://github.com/alecmkrueger/gerg_plotting)



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Alec Krueger, Texas A&M University, Geochemical and Environmental Research Group, alecmkrueger@tamu.edu

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/alecmkrueger/gerg_plotting.svg?style=for-the-badge
[contributors-url]: https://github.com/alecmkrueger/gerg_plotting/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/alecmkrueger/gerg_plotting.svg?style=for-the-badge
[forks-url]: https://github.com/alecmkrueger/gerg_plotting/network/members
[stars-shield]: https://img.shields.io/github/stars/alecmkrueger/gerg_plotting.svg?style=for-the-badge
[stars-url]: https://github.com/alecmkrueger/gerg_plotting/stargazers
[issues-shield]: https://img.shields.io/github/issues/alecmkrueger/gerg_plotting.svg?style=for-the-badge
[issues-url]: https://github.com/alecmkrueger/gerg_plotting/issues
[license-shield]: https://img.shields.io/github/license/alecmkrueger/gerg_plotting.svg?style=for-the-badge
[license-url]: https://github.com/alecmkrueger/gerg_plotting/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/aleckrueger
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/python-000000?&logo=python
[Python-url]: https://www.python.org/