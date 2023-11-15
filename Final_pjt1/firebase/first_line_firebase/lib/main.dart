import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

import 'package:path_provider/path_provider.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

import 'package:firebase_database/firebase_database.dart';
import 'package:firebase_messaging/firebase_messaging.dart';

import 'package:http/http.dart' as http;
import 'dart:convert';


import 'API.dart';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {

  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: ImageMoveApp(),
    );
  }
}

class ImageMoveApp extends StatefulWidget {
  const ImageMoveApp({super.key});

  @override
  _ImageMoveAppState createState() => _ImageMoveAppState();
}

class _ImageMoveAppState extends State<ImageMoveApp> {
  double imageX = 90;
  double imageY = 240;
  String imageUrl = '';
  DateTime currentTime = DateTime.now();

  // Get a reference to the Firestore collection
  // final CollectionReference _reference = FirebaseFirestore.instance.collection('user');
  // ignore: deprecated_member_use


  File? _image;
  
  var uniqueFileName;
  Future getImage() async {
    final image = await ImagePicker().pickImage(source: ImageSource.camera);

    if (image == null) return;
    // final imageFile = File(image.path);

    // Make Unique Name
    uniqueFileName = DateTime.now().microsecondsSinceEpoch.toString();

    /***** FireStore Storage
    // Create a reference to Firebase Storage
    Reference referenceRoot = FirebaseStorage.instance.ref();
    Reference referenceDirImages = referenceRoot.child('images');

    // Create a reference for the image to be stored
    Reference referenceImageToUpload = referenceDirImages.child(uniqueFileName);

    // Handle errors & success
    try{
      // Store the file
      await referenceImageToUpload.putFile(File(image.path));
      // Success : get the download URL
      imageUrl = await referenceImageToUpload.getDownloadURL();
     }catch(error){
      // Some error occured
    }
        // Create a Map of data
      Map<String, dynamic> dataToSend = {
      'name' : uniqueFileName,
      'time' : DateTime.now().toString(),
      'image' : imageUrl,
      };

        // Add a new item
        await _reference.set(dataToSend);
    */

    // Create a reference for the image to be stored
    Reference referenceImageToUpload = FirebaseStorage.instance.ref().child(uniqueFileName);

    // Store the file
    UploadTask uploadTask = referenceImageToUpload.putFile(File(image.path));

    // Wait for the upload to complete
    await uploadTask.whenComplete(() {});

    // Get the download URL
    String downloadUrl = await referenceImageToUpload.getDownloadURL();

    FirebaseDatabase realtime = FirebaseDatabase.instance;
    await realtime.ref().child(uniqueFileName).set({
      "image_url": downloadUrl,
      "time" : DateTime.now().toString(),
      });
  }

  void moveImage(int dx, int dy) {
    setState(() {
      imageX += dx;
      imageY += dy;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[300], // grey[700],
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Big4 FirstLine',
            style: TextStyle(
              fontFamily: 'Lato',
              fontSize: 20,
              color: Colors.black)
              ),
        backgroundColor: Colors.grey[300],
      ),
      body: Center(
        child: Stack(
          children: [
            Positioned.fill(
              child: SizedBox(
                width: 80, // Set the width to your desired size
                height: 80,
                child: Image.asset(
                  'lib/images/maze1.png',
                  fit: BoxFit.cover,
                ),
              ),
            ),
            Positioned.fill(
              child: Image.asset(
              'lib/images/snow1.gif',
              fit: BoxFit.cover,
              ),
            ),
            AnimatedPositioned(
              top: imageY,
              left: imageX,
              duration: const Duration(milliseconds: 300),
              child: SizedBox(
                width: 180,
                height: 180,
                child: Image.asset('lib/images/rudolph.png'),
            ),
            ),
          ],
        ),
      ),
      bottomNavigationBar:
      // children: [
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          IconButton(
            icon: const Icon(Icons.camera_alt, color: Colors.redAccent),
            onPressed: getImage,
          ),
          TextButton(
              onPressed: () async {
                print('API 전 $uniqueFileName');
                Map<String, dynamic> success = await getFastAPIResponse(uniqueFileName);

                for (int i = 0; i < success['direction'].length; i++) {
                  int moveAmount = success['number'][0];
                  if (success['direction'][0] == 'L') {
                    moveImage((-20 * moveAmount), 0);} // Move image left
                  else if (success['direction'][0] == 'R') {
                    moveImage((20 * moveAmount), 0);} // Move image right
                  else if (success['direction'][0] == 'U') {
                    moveImage(0, (-20 * moveAmount));}// Move image up
                  else {
                    moveImage(0, (20 * moveAmount));} // Move image down
                }
              },
              child: const Row(
                children: <Widget> [
                  Text('J', style: TextStyle(color: Colors.orange)),
                  Icon(Icons.grade, color: Colors.orange, size: 20),
                  Icon(Icons.grade, color: Colors.orange, size: 20),
                  Text('N', style: TextStyle(color: Colors.orange)),
                  Text('S', style: TextStyle(color: Colors.orange)),
                ],
              ),
          ),
          TextButton(
            onPressed: () async {
              // YOLO API CODE
              moveImage(0, -65);
              },
              child: const Row(
                children: <Widget>[
                  Text('Y'),
                  Icon(Icons.favorite, color: Colors.lightBlueAccent, size: 20),
                  Text('L'),
                  Icon(Icons.favorite, color: Colors.lightBlueAccent, size: 20),
                  ],
                ),
              ),
            ],
          ),
        );
      }
}
