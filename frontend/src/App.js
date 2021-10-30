import Snapshot from './components/snapshot';
import {Box} from '@mui/material';
import MotorToggle from './components/motorToggle';


function App() {

  return (
    <Box sx={{
      padding            : '100px 50px',
      display            : 'grid',
      gridTemplateColumns: 'repeat(4, 1fr)',
      justifyContent     : 'center',
      alignItems         : 'center',
    }}>
      <div></div>
      <MotorToggle/>
      <Snapshot/>
    </Box>
  );
}

export default App;
