- Example:
  ``` python
  from mcu_mod import *

  mod = mcu(test_mode=False)
  mod.execute()
  ```
- Mod Manifest:
  ``` json
  "mods": {
      "package_name": "example name",
      "version": "0.1.0",
      "runtime": true
  }
- make a Object Animations:
  ``` python
  from mcu_mod.Animations import Animations

  Animations.animate(
    self,
    EaseInOut = 'None',
    PosX = 0,
    PosY = 0
  )
  ```
    


