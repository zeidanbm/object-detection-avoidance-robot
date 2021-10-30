import {useContext, useEffect, useState} from 'react';
import {FormControlLabel, Switch} from '@mui/material';
import {SocketContext} from '../context/socket';


function MotorToggle() {
  const [motorStatus, setMotorStatus] = useState(true);
  const socket = useContext(SocketContext);

  useEffect(() => {
      socket.emit('TOGGLE_MOTOR', motorStatus);
    },
    [
      socket,
      motorStatus,
    ],
  );

  const handleMotorToggle = (event) => {
    setMotorStatus(event.target.checked);
  };

  return (
    <FormControlLabel
      control={
        <Switch
          checked={motorStatus}
          onChange={handleMotorToggle}
        />
      }
      label="Motor Toggle"
    />
  );
}

export default MotorToggle;
