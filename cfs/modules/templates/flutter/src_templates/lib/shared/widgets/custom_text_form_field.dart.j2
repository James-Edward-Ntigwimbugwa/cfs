import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:intl/intl.dart';

import '../../core/mixins/app_theme_mixin.dart';
import 'custom_text.dart';

class CustomInputField extends StatefulWidget {
  final String hintText;
  final String? labelText;
  final int? maxLength;

  // ✅ Paddings
  final EdgeInsets? contentPadding; // inside padding
  final EdgeInsets? fieldPadding; // outside padding

  final TextEditingController controller;
  final TextInputType? keyboardType;
  final Widget? prefix;
  final BoxConstraints? prefixIconConstraint;
  final Widget? suffix;
  final bool? obscureText;
  final bool allowPreviousDates;
  final FormFieldValidator<String?> validator;

  // ✅ Background color
  final Color? bgColor;
  final Color? borderColor;
  final Color? textColor;

  // Input pickers
  final bool isDatePicker;
  final bool isTimePicker;
  final bool isDateTimePicker;
  final bool isImagePicker;
  final bool isDocPicker;

  const CustomInputField({
    super.key,
    required this.hintText,
    this.labelText,
    this.prefix,
    this.suffix,
    this.obscureText = false,
    this.allowPreviousDates = false,
    required this.validator,
    required this.controller,
    this.keyboardType,
    this.maxLength,
    this.contentPadding,
    this.fieldPadding,
    this.isDatePicker = false,
    this.isTimePicker = false,
    this.isDateTimePicker = false,
    this.isImagePicker = false,
    this.isDocPicker = false,
    this.prefixIconConstraint,
    this.bgColor,
    this.borderColor,
    this.textColor,
  });

  @override
  State<CustomInputField> createState() => _CustomInputFieldState();
}

class _CustomInputFieldState extends State<CustomInputField>
    with AppThemeMixin {
  final ImagePicker _picker = ImagePicker();

  Future<void> _handlePick() async {
    if (widget.isDatePicker) {
      DateTime? date = await showDatePicker(
        context: context,
        initialDate: DateTime.now(),
        firstDate: widget.allowPreviousDates ? DateTime(1900) : DateTime.now(),
        lastDate: DateTime(2100),
      );
      if (date != null) {
        widget.controller.text = DateFormat('dd-MM-yyyy').format(date);
      }
    } else if (widget.isTimePicker) {
      TimeOfDay? time = await showTimePicker(
        context: context,
        initialTime: TimeOfDay.now(),
      );
      if (time != null) widget.controller.text = time.format(context);
    } else if (widget.isDateTimePicker) {
      DateTime? date = await showDatePicker(
        context: context,
        initialDate: DateTime.now(),
        firstDate: widget.allowPreviousDates ? DateTime(1900) : DateTime.now(),
        lastDate: DateTime(2100),
      );
      if (date != null) {
        TimeOfDay? time = await showTimePicker(
          context: context,
          initialTime: TimeOfDay.now(),
        );
        if (time != null) {
          final combined = DateTime(
            date.year,
            date.month,
            date.day,
            time.hour,
            time.minute,
          );
          widget.controller.text = DateFormat(
            'dd-MM-yyyy, HH:mm',
          ).format(combined);
        }
      }
    } else if (widget.isImagePicker) {
      final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
      if (image != null) widget.controller.text = image.path;
    } else if (widget.isDocPicker) {
      // TODO: file_picker integration
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: widget.fieldPadding ?? EdgeInsets.zero, // outside padding
      child: TextFormField(
        controller: widget.controller,
        keyboardType: widget.keyboardType,
        obscureText: widget.obscureText ?? false,
        validator: widget.validator,
        style: textTheme.bodyMedium!.copyWith(color: widget.textColor),
        maxLength: widget.maxLength,
        readOnly:
            widget.isDatePicker ||
            widget.isTimePicker ||
            widget.isDateTimePicker ||
            widget.isImagePicker ||
            widget.isDocPicker,
        onTap: () async {
          if (widget.isDatePicker ||
              widget.isTimePicker ||
              widget.isDateTimePicker ||
              widget.isImagePicker ||
              widget.isDocPicker) {
            await _handlePick();
          }
        },
        onTapOutside: (_) => FocusScope.of(context).unfocus(),
        decoration: InputDecoration(
          // ✅ Inside padding
          contentPadding:
              widget.contentPadding ??
              const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          counterText: "",
          hint: CustomText(text: widget.hintText),
          suffixIcon: widget.suffix,
          labelText: widget.labelText,
          prefixIcon: widget.prefix,
          prefixIconConstraints: widget.prefixIconConstraint,
          hintStyle: textTheme.bodyMedium!.copyWith(
            color: colorScheme.onSurface.withAlpha(128),
          ),
          filled: widget.bgColor != null,
          fillColor: widget.bgColor,
          border: OutlineInputBorder(
            borderSide: BorderSide(
              width: .1,
              color: widget.borderColor ?? colorScheme.onSurface,
            ),
            borderRadius: BorderRadius.circular(30),
          ),
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(
              width: .5,
              color: widget.borderColor ?? colorScheme.onSurface,
            ),
            borderRadius: BorderRadius.circular(30),
          ),
        ),
      ),
    );
  }
}
