# Surgical_3D_Reconstruction

## Environment
- Python 2.7
- ROS kinetic
- Ubuntu 16.04

##Usage
- Import "MergeCameras" module
- Download and extract the dataset
- Figure out the timestamp for each camera and get the first 11 numbers as parameters.
- The format of the final output would be a iterator.
- Each iterator consists of a dictionary of following:
```
{
  "kyle_cameras":
  {
    "left_camera_info":"value",
    "left_image_raw":"value",
    "right_camera_info":"value",
    "right_image_raw":"value"
    },
  "melody_cameras":
  {
    "left_camera_info":"value",
    "left_image_raw":"value",
    "right_camera_info":"value",
    "right_image_raw":"value"
  }
}
```
