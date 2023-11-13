import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

import 'package:path_provider/path_provider.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

import 'package:firebase_messaging/firebase_messaging.dart';

import 'package:http/http.dart' as http;
import 'dart:convert';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  // String url;

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
  double imageX = 120;
  double imageY = 300;
  String imageUrl = '';
  DateTime currentTime = DateTime.now();

  // Get a reference to the Firestore collection
  final CollectionReference _reference = FirebaseFirestore.instance.collection('user');

  File? _image;
  Future getImage() async {
    final image = await ImagePicker().pickImage(source: ImageSource.camera);
    if (image == null) return;
    // final imageFile = File(image.path);

    // Make Unique Name
    String uniqueFileName = DateTime.now().microsecondsSinceEpoch.toString();

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
      'time' : Timestamp.now(),
      'image' : imageUrl,
    };

    // Add a new item
    await _reference.add(dataToSend);

  }

  void moveImage(double dx, double dy) {
    setState(() {
      imageX += dx;
      imageY += dy;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.yellow[200],
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Big4 FirstLine',
            style: TextStyle(fontFamily: 'Verdana', fontSize: 25)),
      ),
      body: Center(
        child: Stack(
          children: [
            Positioned(
              top: imageY,
              left: imageX,
              child: Image.asset('lib/images/snowman.png'),
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
            icon: const Icon(Icons.camera_alt),
            onPressed: getImage,
          ),
          IconButton(
            icon: const Icon(Icons.arrow_upward),
            onPressed: () {
              moveImage(0, -20); // Move image up
            },
          ),
          IconButton(
            icon: const Icon(Icons.arrow_downward),
            onPressed: () {
              moveImage(0, 20); // Move image down
            },
          ),
          IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: () {
              moveImage(-20, 0); // Move image left
            },
          ),
          IconButton(
            icon: const Icon(Icons.arrow_forward),
            onPressed: () {
              moveImage(20, 0); // Move image right
            },
          ),
        ],
      ),
      // ],
    );
  }
}
