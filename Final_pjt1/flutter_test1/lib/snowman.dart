import 'dart:math';
import 'package:flutter/material.dart';

class SnowMan extends StatelessWidget {
  // final int snowmanCount;
  final String snowmanDirection;

  // this.snowmanCount,
  SnowMan({Key? key, required this.snowmanDirection});

  @override
  Widget build(BuildContext context) {
    if (snowmanDirection == 'left') {
      return Container(
        alignment: Alignment.bottomCenter,
        // height: 50,
        // width: 50,
        child: Image.asset('lib/images/snowman.png'
        ),
      );
    } else {
      return Transform(
        alignment: Alignment.center,
        transform: Matrix4.rotationY(pi),
        child: Container(
          alignment: Alignment.bottomCenter,
          height: 50,
          width: 50,
          child: Image.asset('lib/images/snowman.png'
          ),
        ),
      );
    }
  }
}

