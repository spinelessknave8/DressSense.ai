import React, { useState, useEffect } from 'react';
import { Button, Image, View, Platform, StyleSheet, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { Camera } from 'expo-camera';
 // Make sure to have the correct path to your upload function here

export default function ImagePickerExample() {
  const [image, setImage] = useState(null);
  const bucketName = 'clothesstorage'; // Your bucket name

  useEffect(() => {
    (async () => {
      if (Platform.OS !== 'web') {
        const cameraStatus = await Camera.requestCameraPermissionsAsync();
        const imagePickerStatus = await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (cameraStatus.status !== 'granted' || imagePickerStatus.status !== 'granted') {
          alert('Sorry, we need camera and media library permissions to make this work!');
        }
      }
    })();
  }, []);

  const uploadImage = async (uri) => {
    const fileName = uri.split('/').pop();
    const fileData = await fetch(uri).then(response => response.blob());
    try {
      await uploadFileToS3(bucketName, fileName, fileData);
      console.log('File Uploaded:', fileName);
      Alert.alert('Success', 'Image uploaded successfully!');
    } catch (error) {
      console.error('Error uploading file:', error);
      Alert.alert('Error', 'Image upload failed');
    }
  };

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images, 
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
      forceJpg: true, // this should convert the heic images from the ios system to the jpeg as needed
    });

    if (!result.cancelled) {
      setImage(result.uri);
      uploadImage(result.uri);
    }
  };

  return (
    <View style={{ flex: 2, alignItems: 'center', justifyContent: 'space-around' }}>
      <Button title="Upload an image from camera roll" onPress={pickImage} />
      {image && <Image source={{ uri: image }} style={{ width: 200, height: 20 }} />}
    </View>
  );
}

const styles = StyleSheet.create({
  // Your styles
});