SELECT cpd.*
FROM cmmi_pixel_data AS cpd
INNER JOIN scattering_geometry_pixel_map AS sgpm
ON cpd.pixel_x = sgpm.pixel_x
AND cpd.pixel_y = sgpm.pixel_y
AND cpd.AOI = sgpm.AOI
AND cpd.AOC = sgpm.AOC
WHERE sgpm.theta_h = 1.8641423465;

SELECT * FROM test.scattering_geometry_pixel_map
WHERE pixel_x = 10 AND pixel_y = 10 AND AOI = 25 and AOC = 90;