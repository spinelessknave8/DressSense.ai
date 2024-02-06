import * as React from 'react';
import { SafeAreaView, StyleSheet } from 'react-native';
import { SegmentedButtons } from 'react-native-paper';
import { Button } from 'react-native-paper';

import { View, Text, TouchableOpacity, FlatList, Image } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';
import { Dimensions } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { GiftedChat } from 'react-native-gifted-chat';

const Stack = createNativeStackNavigator();

// Get the full width of the device
const { width } = Dimensions.get('window');
const outfits = [
  { id: '1', imageUrl: '/Users/etienne/Desktop/IMAGE 2024-02-06 07:15:39.jpg' },
  { id: '2', imageUrl: '/Users/etienne/Desktop/IMAGE 2024-02-06 07:15:34.jpg' },
  { id: '3', imageUrl: '/Users/etienne/Desktop/IMAGE 2024-02-06 07:15:32.jpg' },
  // ... more items
];

const App = () => {

  const renderOutfitItem = ({ item }) => (
    <View style={styles.outfitItemContainer}>
      <Image source={{ uri: item.imageUrl }} style={styles.outfitImage} />
      <TouchableOpacity style={styles.infoButton}>

      </TouchableOpacity>
      <View style={styles.outfitLabelContainer}>
        <Text style={styles.outfitLabelText}>{item.name}</Text>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        {/* ... header content ... */}
      </View>
      <FlatList
        data={outfits}
        renderItem={renderOutfitItem}
        keyExtractor={item => item.id}
        horizontal
        pagingEnabled // This prop enables paging on the FlatList, making it swipeable
        showsHorizontalScrollIndicator={false}
        snapToAlignment="center"
        snapToInterval={110} // Adjust this value to match the width of your items
        decelerationRate="fast"
        contentContainerStyle={styles.outfitsList}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#E1E1E1',
  },
  //headerTitle: {
    //fontSize: 18,
    //fontWeight: '600',
 // },
  outfitsList: {
    flexGrow: 1,
    justifyContent: 'center',
    //alignItems: 'center',
    paddingVertical: 20,
  },
  outfitItemContainer: {
    margin: 10,
    width: width,
    height: 500,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  outfitImage: {
    width: '100%',
    height: '100%',
    borderRadius: 10,
  },
  infoButton: {
    position: 'absolute',
    top: 1,
    right: 1,
    padding: 5,
  },
  outfitLabelContainer: {
    marginTop: 5, // spacing between image and text
    backgroundColor: '#07094C', // blue background color for the box
    paddingHorizontal: 10, // padding on the sides
    paddingVertical: 5, // padding on the top and bottom
    alignItems: 'center',
    justifyContent: 'center',
  },
  outfitLabelText: {
    color: 'white', // text color
    fontWeight: 'bold', // bold text
  },

  //additionalInformationContainer: {
    //marginTop: 5, 
//backgroundColour: '#07094C',
    
  //}
  tabBar: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    borderTopWidth: 1,
    borderTopColor: '#E1E1E1',
    paddingVertical: 10,
  },
  tabItem: {
    alignItems: 'center',
  },
});

export default App;