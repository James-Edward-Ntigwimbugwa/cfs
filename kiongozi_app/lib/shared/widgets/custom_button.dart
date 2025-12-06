import 'package:flutter/material.dart';

import '../../core/theme/app_colors.dart';

class CustomButton extends StatelessWidget {
  final VoidCallback onPressed;
  final Widget child;
  final Color? backgroundColor;
  final Color? textColor;
  final int? borderRadius;
  final EdgeInsets? padding;

  const CustomButton({
    super.key,
    required this.onPressed,
    required this.child,
    this.backgroundColor,
    this.textColor,
    this.borderRadius,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    final Color defaultBg = AppColors.greenMain;
    final Color defaultText = Colors.white;

    return ElevatedButton(
      onPressed: onPressed,
      style: ButtonStyle(
        backgroundColor: WidgetStatePropertyAll(backgroundColor ?? defaultBg),
        foregroundColor: WidgetStatePropertyAll(textColor ?? defaultText),
        elevation: const WidgetStatePropertyAll(0),
        shape: WidgetStatePropertyAll(
          RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
        ),
      ),
      child: child,
    );
  }
}
