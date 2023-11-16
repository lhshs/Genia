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

    // Show loading dialog
    // ignore: use_build_context_synchronously
    showDialog(
  context: context,
  barrierDismissible: false,
  builder: (BuildContext context) {
    return Center(
      child: Container(
        width: 70,
        height: 70,
        decoration: BoxDecoration(
          color: Colors.transparent,
          borderRadius: BorderRadius.circular(10),
        ),
        child: const Padding(
          padding: EdgeInsets.all(12.0),
          child: CircularProgressIndicator(),
        ),
      ),
    );
  },
);

    // Make Unique Name
    uniqueFileName = DateTime.now().microsecondsSinceEpoch.toString();
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

    Navigator.pop(context);

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
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          IconButton(
            icon: const Icon(Icons.camera_alt, color: Colors.redAccent),
            onPressed: getImage,
          ),
          TextButton(
            // Juuns Model
            onPressed: () async {
              print('Succeed To Get API');
              final response = await Juuns_API(uniqueFileName);
              String errorMessage = '';

              if (response.body == 'Internal Server Error') {
                errorMessage = 'Internal Server Error';
              }

              if (errorMessage.contains('Error')) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text(errorMessage, style: const TextStyle(color: Colors.yellowAccent)),
                  duration: const Duration(seconds: 5))
                );
              }
              else {
                final Map<String, dynamic> success = json.decode(response.body);
                for (int i = 0; i < success['direction'].length; i++) {
                  int moveAmount = success['number'][i];
                  
                  for (int j = 0; j < moveAmount; j++) {
                    if (success['direction'][i] == 'L') {
                      moveImage(-15, 0);} // Move image left
                    else if (success['direction'][i] == 'R') {
                      moveImage(15, 0);} // Move image right
                    else if (success['direction'][i] == 'U') {
                      moveImage(0, -15);} // Move image up
                    else {
                      moveImage(0, 15);} // Move image down
                    
                  await Future.delayed(const Duration(milliseconds: 500)); // delay 500 milliseconds
                  }
                  await Future.delayed(const Duration(milliseconds: 500)); // delay 500 milliseconds
                  }
                }
              },
              child: const Row(
                children: <Widget> [
                  Icon(Icons.grade, color: Colors.orange),
                  Text('J', style: TextStyle(color: Colors.orange)),
                  Text('U', style: TextStyle(color: Colors.orange)),
                  Text('U', style: TextStyle(color: Colors.orange)),
                  Text('N', style: TextStyle(color: Colors.orange)),
                  Text('S', style: TextStyle(color: Colors.orange)),
                  Icon(Icons.grade, color: Colors.orange),
              ],
            ),
          ),
          TextButton(
            // Yolo Model
            onPressed: () async {
              print('API 전 $uniqueFileName');
              
              Map<String, dynamic> success = await Yolo_API(uniqueFileName);
              print('Succeed To Get API');
              // print(success['direction'].length);
              String errorMessage = 'Error: ';

              if (success['direction'].length == 0) {
                errorMessage += '"Direction" ';
              } 
              if (success['number'].length == 0) {
                errorMessage += '"Number" ';
              }
              if (success['action'].length == 0) {
                errorMessage += '"Action" ';
              }

              errorMessage += 'value is zero.';
              
              if (errorMessage.contains('Direction') || errorMessage.contains('Number') || errorMessage.contains('Action')) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text(errorMessage, style: const TextStyle(color: Colors.yellowAccent)),
                  duration: const Duration(seconds: 5))
                );
              }  
              else {
                for (int i = 0; i < success['direction'].length; i++) {
                  int moveAmount = success['number'][i];
                  
                  for (int j = 0; j < moveAmount; j++) {
                    if (success['direction'][i] == 'L') {
                      moveImage(-15, 0);} // Move image left
                    else if (success['direction'][i] == 'R') {
                      moveImage(15, 0);} // Move image right
                    else if (success['direction'][i] == 'U') {
                      moveImage(0, -15);} // Move image up
                    else {
                      moveImage(0, 15);} // Move image down
                    
                  await Future.delayed(const Duration(milliseconds: 500)); // delay 500 milliseconds
                  }
                  await Future.delayed(const Duration(milliseconds: 500)); // delay 500 milliseconds
                  }
                }
              },
              child: const Row(
                children: <Widget>[
                  Icon(Icons.favorite, color: Colors.lightBlueAccent),
                  Text('Y'),
                  Text('O'),
                  Text('L'),
                  Text('O'),
                  Icon(Icons.favorite, color: Colors.lightBlueAccent),
                  ],
                ),
              ),
            ],
          ),
        );
      }
}
