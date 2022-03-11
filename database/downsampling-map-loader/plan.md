# Input to function is a set of angles
# TODO: create angle bins
[
    [theta_h, theta_d, phi_d],
    [theta_h, theta_d, phi_d],
    ...
]
# loop over the outer array
    # loop over the inner array
        # find pixels for given angles
        # find MM and average the values
        # TODO: define data and storage


#1. loading up the CSV file that Quinn created. This contains the theta/phi angles per pixel.

#2. Convert the angles (theta/phi) to degrees

#3. Round the three angles to the nearest degree... For theta_h


#(before rounding)
#[theta_d,theta_h,phi_d] (MM) ===> MM

#pixel coord.
#(i,j)  ======> [theta_d,theta_h,phi_d](MM)


#M: [361 x 91 x 91 x 3 x 4 x 4 x However many values are in this bin]


#dont forget to zero things out each time you run a new CMMI file
MM_total = np.zeros(361,91,91,3,4,4);        
MM_total = np.nan;
indx_tracker = np.zeros(361,91,91,3);
for wvs j in range(3):
    for i in range(30):

        #read in the MM
        mm = readCMMI(FilePath) #600 x 600 x 4 x 4

        #Compute the normalized MM
        mm_norm = mm/mm[:,:,0,0];

        #Access the pixel => ang. coord. that Quinn made
        cell = readCell(FilePath)

        #The moving sum. MM.



        for i in range(600):
            for j in range(600):
                #access the angle coord. per pixel
                [theta_d,theta_h,phi_d] = cell(i,j)
                #Get the Mueller matrix at pixel (i,j)
                MM = mm(i,j,:,:)


                #now convert [theta_d,theta_h,phi_d] to downsampled angular coord.
                theta_d_down_idx = np.round(theta_d)
                theta_h_down_idx = find_nearest(array_of_theta_h,theta_h)[0]; #just in the index
                phi_d_down_idx = np.round(phi_d)
               
               
                indx_tracker[theta_d_down_idx,theta_h_down_idx,phi_d_down_idx,wvs] +=1;
                MM_total[theta_d_down_idx,theta_h_down_idx,phi_d_down_idx,wvs,:,:] += MM;






#Computing the average MM per bin
for i in range(361):
for j in range(91):
for k in range(91):
            for m in range(3):
MM_total[i,j,k,m,:,:] = MM_total[i,j,k,m,:,:]/indx_tracker[i,j,k.m];
           
           

#load the pbsdf file

A = tensor.read_tensor(file)

A['M'] = MM_total;

tensor.write_tensor("your new file path",**A);