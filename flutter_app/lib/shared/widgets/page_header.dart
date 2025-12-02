import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:heroicons/heroicons.dart';
import 'package:kiongozi/core/constants/dimensions.dart';
import 'package:kiongozi/core/mixins/app_localization_mixin.dart';

import '../../core/enums/text_type.dart';
import 'custom_text.dart';

class BuildPageHeader extends StatefulWidget {
  final String title;
  final VoidCallback? onTap;
  final bool showIcon; // Optional icon visibility
  final Widget? customAction; // Optional custom widget for right side
  final Widget?
  bottomWidget; // Optional widget below header (for TabBars, etc.)

  const BuildPageHeader({
    super.key,
    required this.title,
    this.onTap,
    this.showIcon = true, // Default to true to not break existing usage
    this.customAction,
    this.bottomWidget,
  });

  @override
  State<BuildPageHeader> createState() => _BuildPageHeaderState();
}

class _BuildPageHeaderState extends State<BuildPageHeader>
    with LocalizationMixin {
  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            GestureDetector(
              onTap: () => context.pop(),
              child: Row(
                spacing: Dimensions.width20,
                children: [
                  HeroIcon(HeroIcons.arrowLeft),
                  CustomText(text: widget.title, textType: TextType.titleText),
                ],
              ),
            ),
            // Show custom action if provided, otherwise show icon if enabled
            if (widget.customAction != null)
              widget.customAction!
            else if (widget.showIcon)
              Container(
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surface,
                  shape: BoxShape.circle,
                ),
                child: IconButton(
                  onPressed: widget.onTap,
                  icon: HeroIcon(
                    HeroIcons.ellipsisVertical,
                    color: Theme.of(context).colorScheme.onSurface,
                  ),
                ),
              ),
          ],
        ),
        // Add bottom widget if provided
        if (widget.bottomWidget != null) widget.bottomWidget!,
      ],
    );
  }
}
