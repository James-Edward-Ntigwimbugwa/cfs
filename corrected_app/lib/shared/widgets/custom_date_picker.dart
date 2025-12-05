import 'package:flutter/material.dart';
import 'package:hugeicons/hugeicons.dart';
import '../../../../core/constants/dimensions.dart';
import '../../core/theme/app_colors.dart';

class CustomDatePicker extends StatelessWidget {
  final String label;
  final DateTime? selectedDate;
  final VoidCallback onTap;
  final bool enabled;
  final String? errorText;
  final DateTime? firstDate;
  final DateTime? lastDate;

  const CustomDatePicker({
    super.key,
    required this.label,
    required this.selectedDate,
    required this.onTap,
    this.enabled = true,
    this.errorText,
    this.firstDate,
    this.lastDate,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        InkWell(
          onTap: enabled ? onTap : null,
          borderRadius: BorderRadius.circular(Dimensions.radius20),
          child: Container(
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
              borderRadius: BorderRadius.circular(Dimensions.radius20),
              border: Border.all(
                color: errorText != null
                    ? Theme.of(context).colorScheme.error
                    : Theme.of(
                        context,
                      ).colorScheme.onSurface.withValues(alpha: 0.3),
                width: 1,
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: .02),
                  blurRadius: 4,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            padding: EdgeInsets.symmetric(
              horizontal: Dimensions.width16,
              vertical: Dimensions.height16,
            ),
            child: Row(
              children: [
                Container(
                  padding: EdgeInsets.all(Dimensions.width8),
                  decoration: BoxDecoration(
                    color: selectedDate != null
                        ? AppColors.greenMain.withOpacity(0.1)
                        : Theme.of(context).colorScheme.surface,
                    shape: BoxShape.circle,
                  ),
                  child: HugeIcon(
                    icon: HugeIcons.strokeRoundedCalendar01,
                    color: AppColors.greenMain,
                    size: Dimensions.iconSize16,
                  ),
                ),
                SizedBox(width: Dimensions.width12),
                Expanded(
                  child: Text(
                    selectedDate != null ? _formatDate(selectedDate!) : label,
                    style: TextStyle(
                      color: Theme.of(
                        context,
                      ).colorScheme.onSurface.withValues(alpha: .7),
                      fontSize: Dimensions.fontSize14,
                      fontWeight: selectedDate != null
                          ? FontWeight.w500
                          : FontWeight.normal,
                    ),
                  ),
                ),
                CircleAvatar(
                  backgroundColor: AppColors.greenMain,
                  maxRadius: Dimensions.radius12 * 0.8,
                  child: ClipOval(
                    child: HugeIcon(
                      icon: selectedDate != null
                          ? HugeIcons.strokeRoundedEdit01
                          : HugeIcons.strokeRoundedAdd01,
                      size: Dimensions.iconSize16 * 0.8,
                      color: Colors.white,
                    ),
                  ),
                ),
              ],
            ),
          ),
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
                color: Theme.of(context).colorScheme.error,
                fontSize: Dimensions.fontSize12,
              ),
            ),
          ),
      ],
    );
  }

  String _formatDate(DateTime date) {
    final months = [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec',
    ];
    return '${date.day} ${months[date.month - 1]} ${date.year}';
  }

  // Helper method to show date picker with custom styling
  static Future<DateTime?> show(
    BuildContext context, {
    DateTime? initialDate,
    DateTime? firstDate,
    DateTime? lastDate,
  }) async {
    return await showDatePicker(
      context: context,
      initialDate: initialDate ?? DateTime.now(),
      firstDate: firstDate ?? DateTime(2020),
      lastDate: lastDate ?? DateTime(2030),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: ColorScheme.light(
              primary: AppColors.greenMain,
              onPrimary: Theme.of(context).colorScheme.onPrimary,
              surface: Theme.of(context).cardColor,
              onSurface: Theme.of(context).colorScheme.onSurface,
            ),
            dialogBackgroundColor: Theme.of(context).colorScheme.onSurface,
          ),
          child: child!,
        );
      },
    );
  }
}
