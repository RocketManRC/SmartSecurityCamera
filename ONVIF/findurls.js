const onvif = require('node-onvif');
const config = require('./config');
const preferences = require('./config');

console.log('Start the discovery process.');
// Find the ONVIF network cameras.
// It will take about 3 seconds.
onvif.startProbe().then((device_info_list) => {
  console.log(device_info_list.length + ' devices were found.\n');
  // Show the device name and the URL of the end point.
  device_info_list.forEach((info) => {
    //console.log('- ' + info.urn);
    //console.log('  - ' + info.name);
    //console.log('  - ' + info.xaddrs[0]);
    
        // Create an OnvifDevice object
    let device = new onvif.OnvifDevice({
      xaddr: info.xaddrs[0],
      //user : 'admin',
      //pass : '123456'
      user : config.user,
      pass : config.pw
    });

    // Initialize the OnvifDevice object
    device.init().then((info) => {
      // Show the detailed information of the device.
      console.log(JSON.stringify(info, null, '  '));
      let url = device.getUdpStreamUrl();
      console.log(url + '\n');
    }).catch((error) => {
      console.error(error);
    });
  });
}).catch((error) => {
  console.error(error);
});
