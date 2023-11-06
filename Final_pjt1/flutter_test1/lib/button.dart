import 'package:flutter/material.dart';

class MyButton extends StatelessWidget {
  final text;
  final function;

  const MyButton({super.key, this.text, this.function});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(10.0),
      child: GestureDetector(
        onTap: function,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(10),
          child: Container(
            padding: const EdgeInsets.all(10),
            color: Colors.grey[800],
            child: Center(
              child: Text(text, style: const TextStyle(color: Colors.white, fontSize: 50)),
            ),
          ),
        ),
      ),
    );
  }
}