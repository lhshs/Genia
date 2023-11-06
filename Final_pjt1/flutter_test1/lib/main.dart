import 'package:flutter/material.dart';
import 'package:flutter_test1/button.dart';

import 'snowman.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget{
  const HomePage({super.key});

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {

  // Snow Man
  double snowmanPosX = -5;
  String snowmanDirection = 'left';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          Expanded(
            flex: 5,
            child: Container(
              color: Colors.blue[300],
              child: Stack(
                children: [
                  Container(
                    alignment: AlignmentDirectional.center,  // (snowmanPosX, 1),
                    child: SnowMan(
                      snowmanDirection: snowmanDirection,
                    ),
                  )
               ],
              ),
            ),
          ),
          // Container(
          //   height: 50,
          //   color: Colors.green[600],
          // ),


          // Expanded(
          //   child: Container(
          //     color: Colors.grey[500],
          //     child: Column(
          //       mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          //       children: [
          //         const Text('Big4 FirstLine',
          //                    style: TextStyle(color: Colors.white,
          //                                     fontSize: 20,
          //                                     fontFamily: 'fantasy')),
          //         // Row(
          //         //   mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          //         //   children: [
          //         //     MyButton(
          //         //       text: '↑',
          //         //       function: () {},
          //         //     ),
          //         //     MyButton(
          //         //       text: '↓',
          //         //       function: () {},
          //         //     ),
          //         //     MyButton(
          //         //       text: '←',
          //         //       function: () {},
          //         //     ),
          //         //     MyButton(
          //         //       text: '→',
          //         //       function: () {},
          //         //     ),
          //         //   ],
          //         //  ),
          //       ],
          //     )
          //   ),
          // ),
        ]),
    );
  }
}