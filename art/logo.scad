$fn=100;
color([2/255,136/255,209/255]) rotate(90) {
translate([0,0])   circle(d=10);
translate([0,20])  circle(d=10);
translate([0,40])  circle(d=10);


translate([45,20]) {
    //Top
    translate([0,17.5])
        square([5,9],center=true);
    
    translate([0,13.5])
    rotate(45) square([5,5], center=true);
    
    translate([-22.5,20])
        square([50,5],center=true);
    
    //Middle
    translate([-25,0])
    square([32.5,5], center=true);
    translate([-8.5,0])
    rotate(45) square([5,5], center=true);
    
    //Bottom
    translate([0,-17.5])
        square([5,9],center=true);
    
    translate([0,-13.5])
    rotate(45) square([5,5], center=true);
    
    translate([-22.5,-20])
        square([50,5],center=true);
    
    square([10,20],center=true);
}
}