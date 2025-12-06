import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/constants/dimensions.dart';
import '../../../../core/mixins/app_theme_mixin.dart';
import '../../../../shared/widgets/custom_button.dart';
import '../../../../shared/widgets/custom_text.dart';
import '../../../../shared/widgets/custom_text_form_field.dart';

class ChangePassword extends StatefulWidget {
  const ChangePassword({super.key});

  @override
  State<ChangePassword> createState() => _ChangePasswordState();
}

class _ChangePasswordState extends State<ChangePassword> with AppThemeMixin {
  final _formKey = GlobalKey<FormState>();
  final oldPasswordController = TextEditingController();
  final newPasswordController = TextEditingController();
  final confirmPasswordController = TextEditingController();
  bool _isLoading = false;

  @override
  void dispose() {
    oldPasswordController.dispose();
    newPasswordController.dispose();
    confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _handleChangePassword() async {
    if (_formKey.currentState?.validate() ?? false) {
      setState(() => _isLoading = true);

      // Simulate API call
      await Future.delayed(const Duration(seconds: 2));

      setState(() => _isLoading = false);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Password changed successfully'),
            backgroundColor: colorScheme.primary,
            behavior: SnackBarBehavior.floating,
          ),
        );
        context.pop();
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: colorScheme.surface,
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            // App Bar
            SliverAppBar(
              pinned: true,
              elevation: 0,
              backgroundColor: colorScheme.surface,
              leading: IconButton(
                icon: Icon(
                  Icons.arrow_back_ios_new,
                  color: colorScheme.onSurface,
                ),
                onPressed: () => context.pop(),
              ),
            ),

            // Content
            SliverFillRemaining(
              hasScrollBody: false,
              child: Padding(
                padding: EdgeInsets.symmetric(horizontal: Dimensions.width24),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      SizedBox(height: Dimensions.height24),

                      // Header Section
                      Text(
                        "Change your password",
                        style: textTheme.displaySmall?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: colorScheme.onSurface,
                        ),
                      ),
                      SizedBox(height: Dimensions.height8),
                      Text(
                        "fill informations below",
                        style: textTheme.bodyLarge?.copyWith(
                          color: colorScheme.onSurfaceVariant,
                        ),
                      ),

                      SizedBox(height: Dimensions.height48),

                      // Old Password Field
                      Text(
                        "old password",
                        style: textTheme.labelLarge?.copyWith(
                          color: colorScheme.onSurface,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      SizedBox(height: Dimensions.height8),
                      CustomInputField(
                        hintText: '••••••••',
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Old password is required';
                          }
                          return null;
                        },
                        controller: oldPasswordController,
                        obscureText: true,
                        prefixIcon: Icon(
                          Icons.lock_outline,
                          color: colorScheme.primary,
                        ),
                      ),

                      SizedBox(height: Dimensions.height20),

                      // New Password Field
                      Text(
                        "New Password",
                        style: textTheme.labelLarge?.copyWith(
                          color: colorScheme.onSurface,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      SizedBox(height: Dimensions.height8),
                      CustomInputField(
                        hintText: '••••••••',
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'New password is required';
                          }
                          if (value.length < 8 || value.length > 20) {
                            return 'Password must be between 8 and 20 characters';
                          }
                          if (!RegExp(r'(?=.*[a-z])').hasMatch(value)) {
                            return 'Password must include at least one lowercase letter';
                          }
                          if (!RegExp(r'(?=.*[A-Z])').hasMatch(value)) {
                            return 'Password must include at least one uppercase letter';
                          }
                          if (!RegExp(r'(?=.*\d)').hasMatch(value)) {
                            return 'Password must include at least one number';
                          }
                          if (!RegExp(
                            r'(?=.*[!@#$%^&*(),.?":{}|<>])',
                          ).hasMatch(value)) {
                            return 'Password must include at least one special character';
                          }
                          return null;
                        },
                        controller: newPasswordController,
                        obscureText: true,
                        prefixIcon: Icon(
                          Icons.lock_reset,
                          color: colorScheme.primary,
                        ),
                      ),

                      SizedBox(height: Dimensions.height20),

                      // Confirm Password Field
                      Text(
                        "Confirm Password",
                        style: textTheme.labelLarge?.copyWith(
                          color: colorScheme.onSurface,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      SizedBox(height: Dimensions.height8),
                      CustomInputField(
                        hintText: '••••••••',
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please confirm your password';
                          }
                          if (value != newPasswordController.text) {
                            return 'Passwords do not match';
                          }
                          return null;
                        },
                        controller: confirmPasswordController,
                        obscureText: true,
                        prefixIcon: Icon(
                          Icons.check_circle_outline,
                          color: colorScheme.primary,
                        ),
                      ),

                      SizedBox(height: Dimensions.height12),

                      // Password Requirements
                      Container(
                        padding: EdgeInsets.all(Dimensions.width12),
                        decoration: BoxDecoration(
                          color: colorScheme.primaryContainer.withOpacity(0.3),
                          borderRadius: BorderRadius.circular(
                            Dimensions.radius12,
                          ),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Password Requirements:',
                              style: textTheme.labelMedium?.copyWith(
                                fontWeight: FontWeight.bold,
                                color: colorScheme.onSurfaceVariant,
                              ),
                            ),
                            SizedBox(height: Dimensions.height4),
                            _buildRequirement('At least 8 characters'),
                            _buildRequirement('One uppercase letter'),
                            _buildRequirement('One lowercase letter'),
                            _buildRequirement('One number'),
                            _buildRequirement('One special character'),
                          ],
                        ),
                      ),

                      const Spacer(),

                      // Change Password Button
                      SizedBox(
                        width: double.infinity,
                        height: Dimensions.height56,
                        child: CustomButton(
                          onPressed: _isLoading
                              ? () {}
                              : () => _handleChangePassword(),
                          child: _isLoading
                              ? SizedBox(
                                  height: 24,
                                  width: 24,
                                  child: CircularProgressIndicator(
                                    color: colorScheme.onPrimary,
                                    strokeWidth: 2,
                                  ),
                                )
                              : CustomText(
                                  color: colorScheme.onPrimary,
                                  text:
                                      "change password", // Fixed typo: "chane" to "change"
                                  style: textTheme.titleMedium?.copyWith(
                                    fontWeight: FontWeight.bold,
                                    color: colorScheme.onPrimary,
                                  ),
                                ),
                        ),
                      ),

                      SizedBox(height: Dimensions.height24),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRequirement(String text) {
    return Padding(
      padding: EdgeInsets.only(top: Dimensions.height4),
      child: Row(
        children: [
          Icon(
            Icons.check_circle,
            size: 14,
            color: colorScheme.primary.withOpacity(0.7),
          ),
          SizedBox(width: Dimensions.width8),
          Text(
            text,
            style: textTheme.bodySmall?.copyWith(
              color: colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ),
    );
  }
}
