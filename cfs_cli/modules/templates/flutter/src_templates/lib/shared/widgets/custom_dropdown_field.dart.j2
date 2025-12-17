import 'package:flutter/material.dart';

import '../../core/mixins/app_theme_mixin.dart';

/// Model for dropdown items
class DropDownItem<T> {
  final T value;
  final Widget label;
  const DropDownItem({required this.value, required this.label});
}

class CustomDropdownFormField<T> extends StatefulWidget {
  final List<DropDownItem<T>> items;
  final String hintText;
  final Widget? prefix;
  final Widget? suffix;
  final EdgeInsets? contentPadding;
  final BoxConstraints? prefixIconConstraint;
  final FormFieldValidator<T>? validator;
  final FormFieldSetter<T>? onSaved;
  final T? initialValue;

  const CustomDropdownFormField({
    super.key,
    required this.items,
    required this.hintText,
    this.prefix,
    this.suffix,
    this.contentPadding,
    this.prefixIconConstraint,
    this.validator,
    this.onSaved,
    this.initialValue,
  });

  @override
  State<CustomDropdownFormField<T>> createState() =>
      _CustomDropdownFormFieldState<T>();
}

class _CustomDropdownFormFieldState<T> extends State<CustomDropdownFormField<T>>
    with AppThemeMixin {
  T? _selectedValue;

  @override
  void initState() {
    super.initState();
    _selectedValue = widget.initialValue;
  }

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<T>(
      value: _selectedValue,
      validator: widget.validator,
      onSaved: widget.onSaved,
      isExpanded: true,
      dropdownColor: colorScheme.surface, // match theme surface
      decoration: InputDecoration(
        contentPadding:
            widget.contentPadding ?? const EdgeInsets.symmetric(horizontal: 12),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(30),
          borderSide: const BorderSide(width: 0.5),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(39),
          borderSide: const BorderSide(width: 0.5),
        ),
        prefixIcon: widget.prefix,
        suffixIcon: widget.suffix,
        prefixIconConstraints: widget.prefixIconConstraint,
        hintText: widget.hintText,
        hintStyle: textTheme.bodySmall!.copyWith(fontWeight: FontWeight.w200),
      ),
      alignment: AlignmentDirectional.centerStart,
      items: widget.items
          .map(
            (item) => DropdownMenuItem<T>(value: item.value, child: item.label),
          )
          .toList(),
      onChanged: (value) {
        setState(() {
          _selectedValue = value;
        });
        if (widget.onSaved != null) {
          widget.onSaved!(value);
        }
        FocusScope.of(context).unfocus();
      },
    );
  }
}
