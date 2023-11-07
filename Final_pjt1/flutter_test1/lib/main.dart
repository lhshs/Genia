import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: ImageMoveApp(),
    );
  }
}

class ImageMoveApp extends StatefulWidget {
  @override
  _ImageMoveAppState createState() => _ImageMoveAppState();
}

class _ImageMoveAppState extends State<ImageMoveApp> {
  double imageX = 120;
  double imageY = 300;

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
        title: Text('Big4 FirstLine',
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
                icon: Icon(Icons.camera_alt),
                onPressed: () {
                  // requestCameraPermission(); // Request camera permission
                  // initializeCamera(); // Initialize the camera
                },
              ),
              IconButton(
                icon: Icon(Icons.arrow_upward),
                onPressed: () {
                  moveImage(0, -20); // Move image up
                },
              ),
              IconButton(
                icon: Icon(Icons.arrow_downward),
                onPressed: () {
                  moveImage(0, 20); // Move image down
                },
              ),
              IconButton(
                icon: Icon(Icons.arrow_back),
                onPressed: () {
                  moveImage(-20, 0); // Move image left
                },
              ),
              IconButton(
                icon: Icon(Icons.arrow_forward),
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




//       Column(
//         mainAxisAlignment: MainAxisAlignment.end,
//         children: [
//           Row(
//             mainAxisAlignment: MainAxisAlignment.spaceEvenly,
//             children: [
//               IconButton(
//                 icon: Icon(Icons.camera_alt),
//                 onPressed: () {
//                   // requestCameraPermission(); // Request camera permission
//                   // initializeCamera(); // Initialize the camera
//                 },
//               ),
//               IconButton(
//                 icon: Icon(Icons.arrow_upward),
//                 onPressed: () {
//                   moveImage(0, -20); // Move image up
//                 },
//               ),
//               IconButton(
//                 icon: Icon(Icons.arrow_downward),
//                 onPressed: () {
//                   moveImage(0, 20); // Move image down
//                 },
//               ),
//               IconButton(
//                 icon: Icon(Icons.arrow_back),
//                 onPressed: () {
//                   moveImage(-20, 0); // Move image left
//                 },
//               ),
//               IconButton(
//                 icon: Icon(Icons.arrow_forward),
//                 onPressed: () {
//                   moveImage(20, 0); // Move image right
//                 },
//               ),
//             ],
//           ),
//         ],
//       ),
//     );
//   }
// }


//
// import 'dart:io';
// import 'package:flutter/material.dart';
// import 'package:image_picker/image_picker.dart';
//
// void main() {
//   runApp(const MyApp());
// }
//
// class MyApp extends StatefulWidget {
//   const MyApp({Key? key}) : super(key: key);
//
//   @override
//   State<MyApp> createState() => _MyAppState();
// }
//
// class _MyAppState extends State<MyApp> {
//   XFile? _image; //이미지를 담을 변수 선언
//   final ImagePicker picker = ImagePicker(); //ImagePicker 초기화
//
//   //이미지를 가져오는 함수
//   Future getImage(ImageSource imageSource) async {
//     //pickedFile에 ImagePicker로 가져온 이미지가 담긴다.
//     final XFile? pickedFile = await picker.pickImage(source: imageSource);
//     if (pickedFile != null) {
//       setState(() {
//         _image = XFile(pickedFile.path); //가져온 이미지를 _image에 저장
//       });
//     }
//   }
//
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       home: Scaffold(
//         appBar: AppBar(title: Text("Camera Test")),
//         body: Column(
//           crossAxisAlignment: CrossAxisAlignment.center,
//           children: [
//             SizedBox(height: 30, width: double.infinity),
//             _buildPhotoArea(),
//             SizedBox(height: 20),
//             _buildButton(),
//           ],
//         ),
//       ),
//     );
//   }
//
//   Widget _buildPhotoArea() {
//     return _image != null
//         ? Container(
//       width: 300,
//       height: 300,
//       child: Image.file(File(_image!.path)), //가져온 이미지를 화면에 띄워주는 코드
//     )
//         : Container(
//       width: 300,
//       height: 300,
//       color: Colors.grey,
//     );
//   }
//
//   Widget _buildButton() {
//     return Row(
//       mainAxisAlignment: MainAxisAlignment.center,
//       children: [
//         ElevatedButton(
//           onPressed: () {
//             getImage(ImageSource.camera); //getImage 함수를 호출해서 카메라로 찍은 사진 가져오기
//           },
//           child: Text("카메라"),
//         ),
//         SizedBox(width: 30),
//         ElevatedButton(
//           onPressed: () {
//             getImage(ImageSource.gallery); //getImage 함수를 호출해서 갤러리에서 사진 가져오기
//           },
//           child: Text("갤러리"),
//         ),
//       ],
//     );
//   }
// }