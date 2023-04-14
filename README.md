# Copying_Virtual_Machine
This Python code is used to clone a virtual machine from a source ESXi server to a destination ESXi server using vSphere object model and PyVmomi library. It first connects to the source ESXi server using the provided credentials and retrieves the content of the vSphere object model. It then locates the specified virtual machine in the inventory tree of the source ESXi server using its name.

Once the virtual machine is located, it creates a new virtual machine configuration based on the source virtual machine's configuration. This configuration includes the number of CPUs, memory size, and the hot-add settings for CPU and memory. It then sets the destination folder for the new virtual machine in the destination ESXi server and renames it by appending "-copy" to the original name.

Next, the code gets the resource pool of the destination ESXi server where the new virtual machine will be created. It creates a relocation specification to specify the target ESXi server and the resource pool. It then creates a clone specification to specify the configuration and relocation of the new virtual machine.

Finally, the code clones the virtual machine from the source ESXi server to the destination ESXi server using the newly created specifications. It waits for the clone task to complete and checks whether it succeeded or failed. If the clone task succeeds, it prints a message stating that the virtual machine was successfully cloned. If the clone task fails, it prints an error message indicating the cause of the failure.

Once the cloning process is complete, the code disconnects from the source ESXi server. Overall, this code provides an easy and efficient way to clone virtual machines from one ESXi server to another using vSphere object model and PyVmomi library.
