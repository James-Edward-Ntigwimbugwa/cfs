import 'package:flutter/material.dart';
import '../../../../core/constants/dimensions.dart';

class CustomTextField extends StatelessWidget {
  final TextEditingController controller;
  final String labelText;
  final String hintText;
  final bool enabled;
  final String? errorText;
  final int maxLines;
  final ValueChanged<String>? onChanged;
  final TextInputType? keyboardType;

  // Additional styling options
  final Color? fillColor;
  final Color? borderColor;
  final Color? focusedBorderColor;
  final Color? labelColor;
  final Color? hintColor;
  final Color? textColor;
  final double? borderRadius;
  final EdgeInsetsGeometry? contentPadding;
  final TextStyle? textStyle;
  final TextStyle? labelStyle;
  final TextStyle? hintStyle;
  final Widget? prefixIcon;
  final Widget? suffixIcon;
  final bool obscureText;
  final int? maxLength;
  final FocusNode? focusNode;

  const CustomTextField({
    super.key,
    required this.controller,
    required this.labelText,
    required this.hintText,
    this.enabled = true,
    this.errorText,
    this.maxLines = 1,
    this.onChanged,
    this.keyboardType,
    this.fillColor,
    this.borderColor,
    this.focusedBorderColor,
    this.labelColor,
    this.hintColor,
    this.textColor,
    this.borderRadius,
    this.contentPadding,
    this.textStyle,
    this.labelStyle,
    this.hintStyle,
    this.prefixIcon,
    this.suffixIcon,
    this.obscureText = false,
    this.maxLength,
    this.focusNode,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDark = theme.brightness == Brightness.dark;

    // Default colors based on theme
    final defaultFillColor = enabled
        ? (isDark ? colorScheme.surface.withOpacity(0.1) : Colors.grey[50])
        : (isDark ? colorScheme.surface.withOpacity(0.05) : Colors.grey[200]);

    final defaultBorderColor = errorText != null
        ? colorScheme.error
        : (isDark ? Colors.grey[700]! : Colors.grey[300]!);

    final defaultFocusedBorderColor = errorText != null
        ? colorScheme.error
        : colorScheme.primary;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TextField(
          controller: controller,
          enabled: enabled,
          maxLines: maxLines,
          maxLength: maxLength,
          keyboardType: keyboardType,
          obscureText: obscureText,
          style:
              textStyle ??
              TextStyle(
                color: textColor ?? colorScheme.onSurface,
                fontSize: Dimensions.fontSize14,
              ),
          decoration: InputDecoration(
            labelText: labelText,
            labelStyle:
                labelStyle ??
                TextStyle(
                  color:
                      labelColor ??
                      colorScheme.onSurface.withValues(alpha: 0.7),
                  fontSize: Dimensions.fontSize14,
                ),
            hintText: hintText,
            hintStyle:
                hintStyle ??
                TextStyle(
                  color:
                      hintColor ??
                      (isDark ? Colors.grey[500] : Colors.grey[400]),
                  fontSize: Dimensions.fontSize14,
                ),
            prefixIcon: prefixIcon,
            suffixIcon: suffixIcon,
            filled: true,
            fillColor: fillColor ?? defaultFillColor,
            counterText: maxLength != null ? null : '',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(
                borderRadius ?? Dimensions.radius20,
              ),
              borderSide: BorderSide(color: borderColor ?? defaultBorderColor),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(
                borderRadius ?? Dimensions.radius20,
              ),
              borderSide: BorderSide(color: borderColor ?? defaultBorderColor),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(
                borderRadius ?? Dimensions.radius20,
              ),
              borderSide: BorderSide(
                color: focusedBorderColor ?? defaultFocusedBorderColor,
                width: 1.5,
              ),
            ),
            disabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(
                borderRadius ?? Dimensions.radius20,
              ),
              borderSide: BorderSide(
                color: isDark ? Colors.grey[800]! : Colors.grey[300]!,
              ),
            ),
            errorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(
                borderRadius ?? Dimensions.radius20,
              ),
              borderSide: BorderSide(color: colorScheme.error),
            ),
            focusedErrorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(
                borderRadius ?? Dimensions.radius20,
              ),
              borderSide: BorderSide(color: colorScheme.error, width: 1.5),
            ),
            contentPadding:
                contentPadding ??
                EdgeInsets.symmetric(
                  horizontal: Dimensions.width20,
                  vertical: Dimensions.height16,
                ),
          ),
          onChanged: onChanged,
        ),
        if (errorText != null)
          Padding(
            padding: EdgeInsets.only(
              top: Dimensions.height4,
              left: Dimensions.width12,
            ),
            child: Text(
              errorText!,
              style: TextStyle(
                color: colorScheme.error,
                fontSize: Dimensions.fontSize12,
              ),
            ),
          ),
      ],
    );
  }
}
