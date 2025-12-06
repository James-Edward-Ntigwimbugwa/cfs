import 'package:flutter/material.dart';

class BottomLeftCircleClipper extends CustomClipper<Path> {
  @override
  Path getClip(Size size) {
    Path path = Path();
    // start from top-left
    path.moveTo(0, 0);
    // top-right
    path.lineTo(size.width, 0);
    // bottom-right
    path.lineTo(size.width, size.height);
    // bottom-left curve
    path.quadraticBezierTo(0, size.height, 0, size.height * 0.5);
    // back to top-left
    path.lineTo(0, 0);
    path.close();
    return path;
  }

  @override
  bool shouldReclip(covariant CustomClipper<Path> oldClipper) => false;
}
