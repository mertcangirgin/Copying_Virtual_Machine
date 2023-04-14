import time
from pyVim import connect
from pyVmomi import vim

# Connect to the source ESXi server using the provided credentials
si = connect.SmartConnectNoSSL(host='<source_esxi_ip>', user='<username>', pwd='<password>')

# Retrieve the content of the vSphere object model
content = si.RetrieveContent()

# Get the root folder of the inventory tree
root_folder = content.rootFolder

# Find the virtual machine in the inventory tree by its name
vm_name = '<vm_name>'
vm = None
for child in root_folder.childEntity:
    if hasattr(child, 'vmFolder'):
        vm_folder = child.vmFolder
        vm_list = vm_folder.childEntity
        for virtual_machine in vm_list:
            if virtual_machine.name == vm_name:
                vm = virtual_machine
                break

# Get the destination ESXi server's IP address or hostname
dest_host = '<destination_esxi_ip>'

# Create a new virtual machine configuration based on the source virtual machine's configuration
config_spec = vim.vm.ConfigSpec()
config_spec.numCPUs = vm.config.hardware.numCPU
config_spec.memoryMB = vm.config.hardware.memoryMB
config_spec.cpuHotAddEnabled = vm.config.cpuHotAddEnabled
config_spec.memoryHotAddEnabled = vm.config.memoryHotAddEnabled

# Get the destination folder for the new virtual machine
dest_folder = content.rootFolder.childEntity[0].vmFolder

# Set the name for the new virtual machine by adding '-copy' to the source virtual machine's name
dest_name = vm_name + '-copy'

# Get the resource pool of the destination ESXi server
resource_pool = None
for rp in content.rootFolder.childEntity[0].resourcePool.resourcePool:
    if rp.name == 'Resources':
        resource_pool = rp
        break

# Create a relocation specification to specify the destination ESXi server and resource pool
relocate_spec = vim.vm.RelocateSpec()
relocate_spec.pool = resource_pool

# Create a clone specification to specify the new virtual machine's configuration and relocation specification
clone_spec = vim.vm.CloneSpec()
clone_spec.location = relocate_spec
clone_spec.config = config_spec

# Clone the virtual machine to the destination ESXi server
task = vm.Clone(name=dest_name, folder=dest_folder, spec=clone_spec)

# Wait for the cloning task to complete
while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
    time.sleep(1)

# Check if the cloning task was successful or not
if task.info.state == vim.TaskInfo.State.error:
    print('An error occurred while cloning the virtual machine:', task.info.error)
else:
    print('The virtual machine was successfully cloned.')

# Disconnect from the source ESXi server
connect.Disconnect(si)
