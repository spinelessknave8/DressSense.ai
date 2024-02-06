import { StatusBar } from 'expo-status-bar';
import { Platform, StyleSheet } from 'react-native';
import * as React from 'react';

import EditScreenInfo from '@/components/EditScreenInfo';
import { Text, View } from '@/components/Themed';

import { SegmentedButtons } from 'react-native-paper';
import { Button } from 'react-native-paper';

const MyComponent = () => {
  const [filtervalue1, filterValue1] = React.useState('');
  const [filtervalue2, filterValue2] = React.useState(false);

  return (
    <View style={styles.container}>
      <SegmentedButtons style={styles.segmentedbuttons1}
        value={filtervalue1}
        onValueChange={filterValue1}
        buttons={[
          {
            value: 'light',
            label: 'Light',
          },
          {
            value: 'dark',
            label: 'Dark',
          },
        ]}
      />



    <SegmentedButtons style={styles.segmentedbuttons2}
        value={filtervalue2}
        onValueChange={filterValue2}
        buttons={[
          {
            value: 'Formal',
            label: 'Formal',
          },
          {
            value: 'Casual',
            label: 'Casual',
          },
          {
            value: 'Sports',
            label: 'Sports',
          },
          {
            value: 'Home',
            label: 'Home',
          }

        ]}
      />

        <Button mode="outlined"
        style={styles.clearbutton}
        textColor='black' >
        Clear
      </Button>

      <Button mode="contained"
        style={styles.applybutton}
        buttonColor='lightskyblue'
        textColor='black' >
        Apply
      </Button>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
  },

  segmentedbuttons1: {
    textColor: 'blue',
    checkedColor: 'lightskyblue',
    uncheckedColor: 'black',
    position: 'absolute',
    alignItems: 'center',
    justifyContent: 'space-evenly',
    fontSize: 10,
    top: 100,
    width: '90%',
  },

  segmentedbuttons2: {
    textColor: 'blue',
    checkedColor: 'lightskyblue',
    uncheckedColor: 'black',
    position: 'absolute',
    alignItems: 'center',
    justifyContent: 'space-evenly',
    fontSize: 10,
    top: 300,
    width: '90%',
  },
  clearbutton: {
    position: 'absolute',
    left: 75,
    bottom: 125,
  },
  applybutton: {
    position: 'absolute',
    right: 75,
    bottom: 125,
  },


});

export default MyComponent;
