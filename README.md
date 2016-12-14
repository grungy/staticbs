# static-bs
A simple 3D electro-magnetostatic biot-savart solving simulator written in python.

No dependencies beyond numpy and scipy

Sometimes you don't want a giant framework. Sometimes you just want some quick and easy bs!

**Authors:** Josh Marks and Andrea Waite
****
### What questions can static-bs answer?

Static-bs can answer questions like these:

- What is the B field at a specific point for a coil of wire without having to use a large volume of points like a finite element solver?
- What does that 3D field look like?
- How does the B field change if I have a bunch of coils oriented in a bunch of different ways?
- What is the electric field if I have charged particles moving through the B field?
- What is the voltage field I see from this electric field?

### What is static-bs not good at doing?

- Evaluating a large number of points or a lot of line segments quickly


### How do you use this fangled thing?

1. ##### Start in the main.py file

   Here you will find the setup for the observation grid and the definition for the
amount of current and number of loops in the coil. The observation grid is the
points where the B field will be evaluated.

   1. Adjust the observation grid to the dimensions and point density that you require
  2. If you don't care about looking at one of the dimensions you can speed up processing
  time by not including it. Look for the section in the code called "Example for how to ignore the z axis."

   3. Set the current you would like in each loop of the coil

   4. Don't forget to save your data by calling 'sim_obj.save()' at the end of the file.

2. #### Setting up your simulation object

   The simulation object represents a unique experiment. It is meant for you to have a copy of this file for each different simulation. In this class you setup the different coils, the placement of the coils, and any other physical constants.

   1. **You will most likely only have to change the coil definition in the class**
   2. Currently, there is a polygon class that can make regular polygons to approximate your coil shape.
   3. If you need a non-regular polygon shape create a class that returns the vertices of that shape.

3. #### Run main.py from the command line

4. #### Visualize your results by using plot.py
   1. Plot.py takes two command line arguments:
      * the location of the B field data
      * the location of the E field data if applicable


### Output examples

#### B field plot of two regular octagons with a radius of 71.53mm in Helmholtz coil configuration
![B field plot of two regular octagons with a radius of 71.53mm in Helmholtz coil configuration]( https://github.com/grungy/static-bs/blob/master/imgs/regular_octagon_helmholtz_71.53mm_radius.png)

#### E field plot of two regular octagons with a radius of 71.53mm in a Helmholtz coil configuration and a fluid moving uniformly in the x direction at 1cm / s
![E field plot of two regular octagons with a radius of 71.53mm in a Helmholtz coil configuration and a fluid moving uniformly in the x direction at 1cm / s](https://github.com/grungy/static-bs/blob/master/imgs/regular_octagon_helmholtz_71.53mm_radius_e_field.png)

### How does static-bs work?

Static-bs works by solving the biot-savart law for finite line segments. The exact solution Static-bs uses can be found on page 9-4 (page 4 in the pdf) of this [course notes guide from MIT](http://web.mit.edu/viz/EM/visualizations/coursenotes/modules/guide09.pdf). Look for the section titled: "Example 9.1: Magnetic Field due to a Finite Straight Wire."

The vertices returned by the polygon class or a user created class are used to create straight wire segments. The B fields from these segments are then vector added together to obtain the final answer.


### Things that still need to be done

1. Possibly change the simulation object architecture so users don't have to edit a class.

2. Update plot.py to automagically determine which axis you might have ignored and plot appropriately.

3. Update the save function in simulation object to accept file names

4. Generally clean up the code by removing my application specific code from it.

5. Implement some kind of SVG gobbling class, so coils can be drawn and easily imported

6. Time varying solutions?
