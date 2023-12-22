
# Mal's VRM Toolkit - Blender Edition

Alternative Version of Mal's VRM0 Utility, but this time for Pure Blender users. 
Extends VRM Addon for Blender, and combines [Przemir's ApplyModifierForObjectWithShapeKeys](https://github.com/przemir/ApplyModifierForObjectWithShapeKeys)

This set of tools allows you streamline both binding of Shapekeys into blendshape proxies, and fix usual errors with VRM reference T-Pose.

Comes with an button to spawn an reference VRM Armature, modified to work with VSeeFace


# Dependencies

- Blender 3.3 or Later. (Tested on Blender 4.0 and 3.6... 3.3 has not been tested.)

- [VRM Addon for Blender](https://vrm-addon-for-blender.info/en/)

- (Built-In) [Przemir's ApplyModifierForObjectWithShapeKeys](https://github.com/przemir/ApplyModifierForObjectWithShapeKeys) dependency to address retargeting to armature

# Installing

Open the Github page, Go to releases and download the `io_extended_scene_vrm_#.#.#.zip` zip file. 

In Blender. Goto `User Preferences`, and `Add-ons`. From there `Install Add-on from File` and select the Zip file that we downloaded.

Enable the plugin under `Addon Extension: Mal's Extended VRM`.


# Tools

[Youtube Demonstration](https://www.youtube.com/watch?v=qkvUbljGmYA)


The Addon adds a new Toolshelf on the Right hand side of the 3D view `VRM0 MalAv Tools`. 
Additional Context sensative tool Panels appear on the Left when editing the Pose of Armature, or editing bones.


## **VRM0 MalAv Tools** 
_Right Hand Tab_ appears on the Right hand side. Panel appears when it is selected. Full feature set available if a VRM0 Armature is selected.

### VRM0.x Armature Extra  Tools

- **Create Reference VRM Armature** - Creates a T-Pose Reference skeleton of the height of 1.77m. Shows Reference Rolls one should match with their avatar.

When VRM Armature is selected:
- **Test T-Pose** - Uses the VRM Armature Bindings to set the avatar into the reference T-Pose. You can use this to debug the armature, and iterate on the rolls and positions of position of the skeleton in order to get it look correctly.
- **Finalize T-Pose** - Aggressively Bakes down all shapekeys to the reference pose on a a clone of the selected visible.
    - Clones selected armature, and all it's visible children, incase of failure/restoration
    - Moves these duplicates to a VRM-T-Pose collection, 
    - Post fixes duplicates with -VRM. 
    - Applies the Above Test T-Pose as the armature's new Rest Pose
    - Bakes the new restpose to <ins>EVERY</ins> single Shapekey of all the visible child mesh. (May take a while)


### VRM0.x Blendshape Proxy Extra Tools

- **Generate and Bind XXXX Shapekeys** - Myriad of Variants: Generates AND Binds Shapekeys to Blendshape Proxy
Supported shapekey sets:
    - VRM
    - VSeeFace extended
    - VRC -> VSF
    - ARKit (iPhone Face Tracking)
    - Meta (Quest Pro Face Tracking)
    - HTC Face Tracking
- **Bind MMD Shapekeys** - Generates Shapekeys ONLY if they exist in the mesh, as accoriding to a list of existing MMD terms.
- **Clear All Blendshape Proxy Binds** - Clears <ins>ALL</ins> Blendshape Proxy Binds . Handy when doing everything from scratch.

### VRM0x Springbone Extra Tools

_Left Hand Panel_ that only appear while in `POSE_ARMATURE` or `EDIT_ARMATURE` modes.

- **Add Selected as SpringboneGroup** - Adds all the selected bones into a <ins>single SpringBone group</ins>
- **Add Selected as Colliders** - Adds all the selected bones as <ins>Individual Colliders</ins>. Adds Colliders to Springbone groups.
- **Clear Springbone Groups** -  Clears ALL the springbone groups 
- **Clear Springbone Collider Groups** -  Clears ALL the Colliders 


# Developing / Contributing

Make sure to use `git submodule init` and `git submodule update` as we are using an external add on to bind shapekeys to new model.

Copy `io_extended_scene_vrm` folder to your Blender Addons Directory. 

On Windows this is under `%APPDATA%/Blender Foundation/Blender/<BlenderVersion>/addons`

If you are using VSCode, I  HIGHLY suggest using **Jacques Lucke's Blender Development Addon** (`JacquesLucke.blender-development`), which allows you to build, redeploy and debug blender add ons directly from the VSCode Workspace.

# Donations

If you think my stuff is neat, feel free to check my other work at my [ko-fi at malactus](https://ko-fi.com/malactus) and maybe buy me a coffee, or two.


# Change Log
### Version 0.0.5
- Fixed more misunderstood reference issues with thumbs related to coordinates being different. Now Matches VRM Addon's reference.

### Version 0.0.4
- Spring Bone Colliders now bind onto existing Spring bones (when created)
- Adjusted scale of Sprinbone colliders

### Version 0.0.2
- Fixed Issues with Thumbs matching a misunderstood VRM reference. Thumbs now use the 45 degree X + 45 degree Z Rule.

### Version 0.0.1
- Initial Version with majority of the features