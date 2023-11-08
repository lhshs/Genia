import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: CameraApp(),
    );
  }
}

class CameraApp extends StatefulWidget {
  const CameraApp({super.key});

  @override
  _CameraAppState createState() => _CameraAppState();
}

class _CameraAppState extends State<CameraApp> {
  late CameraController controller;
  late List<CameraDescription> cameras;

  @override
  void initState() {
    super.initState();
    initializeCamera();
  }

  void initializeCamera() async {
    cameras = await availableCameras();
    controller = CameraController(cameras[0], ResolutionPreset.high);

    await controller.initialize();
    if (!mounted) return;
    setState(() {});
  }

  Future<void> takePicture() async {
    if (controller.value.isTakingPicture) {
      return;
    }

    final directory = await getExternalStorageDirectory();
    final String timestamp = DateTime.now().toIso8601String();
    final String filePath = '${directory!.path}/$timestamp.png';

    try {
      await controller.takePicture(filePath);
      print('Picture saved to $filePath');
      // If you want to save to the gallery, you may need to use a package like image_gallery_saver.
    } catch (e) {
      print('Error taking picture: $e');
    }
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!controller.value.isInitialized) {
      return Container();
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Camera App'),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            Expanded(
              child: CameraPreview(controller),
            ),
            ElevatedButton(
              onPressed: takePicture,
              child: const Icon(Icons.camera),
            ),
          ],
        ),
      ),
    );
  }
}
