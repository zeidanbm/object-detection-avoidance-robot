import {useCallback, useContext, useEffect, useState} from 'react';
import {Box, Button} from '@mui/material';
import {SocketContext} from '../context/socket';


function Snapshot() {
  const [snapshot, setSnapshot] = useState('');

  const socket = useContext(SocketContext);

  const onImageReceived = useCallback(() => {
    setSnapshot('test');
  }, []);

  const handleSnapshotTrigger = useCallback(() => {
    socket.emit('TRIGGER_SNAPSHOT', 1);
  }, [socket]);

  useEffect(() => {
      socket.on('TAKE_SNAPSHOT', onImageReceived);

      return () => {
        // before the component is destroyed
        // unbind all event handlers used in this component
        socket.off('TAKE_SNAPSHOT', onImageReceived);
      };
    },
    [
      socket,
      onImageReceived,
    ],
  );

  return (
    <Box sx={{
      display      : 'flex',
      flexDirection: 'column',
      alignItems   : 'center',
    }}>
      <img
        style={{
          maxWidth    : '250px',
          maxHeight   : '250px',
          marginBottom: '15px',
        }}
        src={snapshot || 'https://via.placeholder.com/250'}
        alt="snapshot"
      />
      <Button variant="contained" onClick={handleSnapshotTrigger}>Take Snapshot</Button>
    </Box>

  );
}

export default Snapshot;
