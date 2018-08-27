CARLA Simulator
===============

Extra
---

Setup instructions: [Google Doc](https://docs.google.com/document/d/1DGxofOAwOq62EJRZKcxoH4oP-T0bvF62KYW_V57ilv4/edit)  
Do pip/pip3 install for requirements  
`sudo pip install -r requirements.txt`  
`sudo pip3 install -r requirements.txt`  
To run Carla:  
`~/UnrealEngine_4.18/Engine/Binaries/Linux/UE4Editor /home/zhefanye/catkin_ws/src/carla/Unreal/CarlaUE4/CarlaUE4.uproject`


[![Build Status](https://travis-ci.org/carla-simulator/carla.svg?branch=master)](https://travis-ci.org/carla-simulator/carla)
[![Documentation](https://readthedocs.org/projects/carla/badge/?version=latest)](http://carla.readthedocs.io)
[![Waffle.io](https://badge.waffle.io/carla-simulator/carla.svg?columns=Next,In%20Progress,Review)](https://waffle.io/carla-simulator/carla)

### Carla is hiring! [Software Engineer](http://www.cvc.uab.es/?p=3853)

[![carla.org](Docs/img/btn/web.png)](http://carla.org)
[![download](Docs/img/btn/download.png)](https://github.com/carla-simulator/carla/releases/latest)
[![documentation](Docs/img/btn/docs.png)](http://carla.readthedocs.io)
[![discord](Docs/img/btn/chat.png)](https://discord.gg/vNVHXfb)
<!-- [![forum](Docs/img/btn/forum.png)](link here) -->

CARLA is an open-source simulator for autonomous driving research. CARLA has
been developed from the ground up to support development, training, and
validation of autonomous urban driving systems. In addition to open-source code
and protocols, CARLA provides open digital assets (urban layouts, buildings,
vehicles) that were created for this purpose and can be used freely. The
simulation platform supports flexible specification of sensor suites and
environmental conditions.

[![CARLA Video](Docs/img/video_thumbnail.png)](https://youtu.be/Hp8Dz-Zek2E)

If you want to benchmark your model in the same conditions as in our CoRL’17
paper, check out
[Benchmarking](http://carla.readthedocs.io/en/latest/benchmark_start/).

News
----

- 23.04.2018 CARLA 0.8.2 released: [post](http://carla.org/2018/04/23/release-0.8.2/), [change log](https://github.com/carla-simulator/carla/blob/master/CHANGELOG.md#carla-082), [release](https://github.com/carla-simulator/carla/releases/tag/0.8.2).
- 05.04.2018 CARLA 0.8.1 released: [post](http://carla.org/2018/04/05/release-0.8.1/), [change log](https://github.com/carla-simulator/carla/blob/master/CHANGELOG.md#carla-081), [release](https://github.com/carla-simulator/carla/releases/tag/0.8.1).
- 27.03.2018 CARLA 0.8.0 released: [post](http://carla.org/2018/03/27/release-0.8.0/), [change log](https://github.com/carla-simulator/carla/blob/master/CHANGELOG.md#carla-080), [release](https://github.com/carla-simulator/carla/releases/tag/0.8.0).
- 25.01.2018 CARLA 0.7.1 released: [change log](https://github.com/carla-simulator/carla/blob/master/CHANGELOG.md#carla-071), [release](https://github.com/carla-simulator/carla/releases/tag/0.7.1).

Roadmap
-------

We are continuously working on improving CARLA, and we appreciate contributions
from the community. Our most immediate goals are:

- [ ] Releasing the methods evaluated in the CARLA paper
- [x] Adding a Lidar sensor
- [ ] Allowing for flexible and user-friendly import and editing of maps
- [ ] Allowing the users to control non-player characters (and therefore set up user-specified scenarios)

Paper
-----

If you use CARLA, please cite our CoRL’17 paper.

_CARLA: An Open Urban Driving Simulator_<br>Alexey Dosovitskiy, German Ros,
Felipe Codevilla, Antonio Lopez, Vladlen Koltun; PMLR 78:1-16
[[PDF](http://proceedings.mlr.press/v78/dosovitskiy17a/dosovitskiy17a.pdf)]


```
@inproceedings{Dosovitskiy17,
  title = {{CARLA}: {An} Open Urban Driving Simulator},
  author = {Alexey Dosovitskiy and German Ros and Felipe Codevilla and Antonio Lopez and Vladlen Koltun},
  booktitle = {Proceedings of the 1st Annual Conference on Robot Learning},
  pages = {1--16},
  year = {2017}
}
```

Building CARLA
--------------

Use `git clone` or download the project from this page. Note that the master
branch contains the latest fixes and features, for the latest stable code may be
best to switch to the latest release tag.

Then follow the instruction at [How to build on Linux][buildlinuxlink] or
[How to build on Windows][buildwindowslink].

Unfortunately we don't have official instructions to build on Mac yet, please
check the progress at [issue #150][issue150].

[buildlinuxlink]: http://carla.readthedocs.io/en/latest/how_to_build_on_linux
[buildwindowslink]: http://carla.readthedocs.io/en/latest/how_to_build_on_windows
[issue150]: https://github.com/carla-simulator/carla/issues/150

Contributing
------------

Please take a look at our [Contribution guidelines][contriblink].

[contriblink]: http://carla.readthedocs.io/en/latest/CONTRIBUTING

F.A.Q.
------

If you run into problems, check our
[FAQ](http://carla.readthedocs.io/en/latest/faq/).

License
-------

CARLA specific code is distributed under MIT License.

CARLA specific assets are distributed under CC-BY License.

Note that UE4 itself follows its own license terms.
