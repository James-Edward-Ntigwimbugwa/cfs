import 'package:flutter/material.dart';
import 'package:flutter_platform_widgets/flutter_platform_widgets.dart';

import '../../core/enums/text_type.dart';

class CustomText extends StatelessWidget {
  final TextType? textType;
  final String text;
  final Color? color;
  final int? maxLines;
  final TextOverflow? overflow;
  final TextAlign? textAlign;
  final FontWeight? fontWeight;
  final double? fontSize;
  final double? letterSpacing;
  final double? lineHeight;
  final TextDecoration? decoration;
  final Color? decorationColor;
  final double? decorationThickness;
  final FontStyle? fontStyle;
  final bool? softWrap;
  final TextDirection? textDirection;
  final Locale? locale;
  final String? fontFamily;
  final List<Shadow>? shadows;
  final double? wordSpacing;

  const CustomText({
    super.key,
    this.textType = TextType.bodyText,
    required this.text,
    this.color,
    this.maxLines,
    this.overflow,
    this.textAlign,
    this.fontWeight,
    this.fontSize,
    this.letterSpacing,
    this.lineHeight,
    this.decoration,
    this.decorationColor,
    this.decorationThickness,
    this.fontStyle,
    this.softWrap,
    this.textDirection,
    this.locale,
    this.fontFamily,
    this.shadows,
    this.wordSpacing,
    TextStyle? style,
  });

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    // Base style based on textType
    TextStyle baseStyle = TextType.titleText == textType
        ? textTheme.titleMedium!.copyWith(
            fontWeight: FontWeight.w500,
            color: color,
          )
        : TextType.labelText == textType
        ? textTheme.labelMedium!.copyWith(
            fontWeight: FontWeight.w300,
            color: color,
          )
        : textTheme.bodyMedium!.copyWith(
            fontWeight: FontWeight.w300,
            color: color,
          );

    // Apply all optional styling
    final TextStyle finalStyle = baseStyle.copyWith(
      fontWeight: fontWeight ?? baseStyle.fontWeight,
      fontSize: fontSize,
      letterSpacing: letterSpacing,
      height: lineHeight,
      decoration: decoration,
      decorationColor: decorationColor,
      decorationThickness: decorationThickness,
      fontStyle: fontStyle,
      fontFamily: fontFamily,
      shadows: shadows,
      wordSpacing: wordSpacing,
    );

    return PlatformText(
      text,
      maxLines: maxLines,
      overflow: overflow,
      textAlign: textAlign,
      softWrap: softWrap,
      textDirection: textDirection,
      locale: locale,
      style: finalStyle,
    );
  }
}
