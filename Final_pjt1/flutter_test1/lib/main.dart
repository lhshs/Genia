import 'dart:io';
import 'package:flutter/material.dart';
import 'package:gallery_saver/gallery_saver.dart';
import 'package:image_picker/image_picker.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';

void main() => runApp(const MyApp());

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
  double imageX = 120;
  double imageY = 300;

  File? _image;
  Future getImage() async {
    final image = await ImagePicker().pickImage(source: ImageSource.camera);
    if (image == null) return;
    final imageTemporary = File(image.path);
    setState(() {
      _image = imageTemporary;
    });
    final savedImagePath = await saveImage(imageTemporary);
    // print('Image saved to: $savedImagePath');
  }

  Future<String?> saveImage(File imageFile) async {
    final directory = await getApplicationDocumentsDirectory();
    final folderPath = '${directory.path}/user_images';
    await Directory(folderPath).create(recursive: true);
    final fileName = imageFile.path;
    final filePath = '$folderPath/$fileName';
    await GallerySaver.saveImage(filePath);
    return filePath;
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

