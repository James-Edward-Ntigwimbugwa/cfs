import 'package:flutter/material.dart';
import 'package:kiongozi/core/constants/dimensions.dart';
import 'package:kiongozi/core/theme/modes/app_colors.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class RadialChart extends StatelessWidget {
  final List<Map<String, dynamic>> data;

  const RadialChart({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: Dimensions.screenWidth,
      constraints: const BoxConstraints(maxWidth: 400),
      padding: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 5),
      margin: const EdgeInsets.only(bottom: 15.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20.0),
        border: Border.all(color: Colors.grey.shade200),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withAlpha((0.08 * 255).toInt()),
            spreadRadius: 0,
            blurRadius: 15,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: SfCircularChart(
        legend: const Legend(
          isVisible: true,
          position: LegendPosition.bottom,
          overflowMode: LegendItemOverflowMode.wrap,
          alignment: ChartAlignment.near,
          padding: 20,
        ),
        series: <RadialBarSeries<Map<String, dynamic>, String>>[
          RadialBarSeries<Map<String, dynamic>, String>(
            dataSource: data,
            xValueMapper: (Map<String, dynamic> data, _) => data['name'],
            yValueMapper: (Map<String, dynamic> data, _) =>
                data['count'].toDouble(),
            dataLabelSettings: const DataLabelSettings(isVisible: true),
            pointColorMapper: (Map<String, dynamic> data, int index) =>
                _getUniqueColor(index),
            maximumValue: _getMaxValue(),
            radius: '100%',
            innerRadius: '50%',
            trackColor: Colors.grey.shade300,
          ),
        ],
      ),
    );
  }

  Color _getUniqueColor(int index) {
    const List<Color> uniqueColors = [
      AppColors.greenMain,
      Color(0XFFE6D49D),
      Color(0xFF323333),
      Color(0XFF667ED7),
    ];

    if (index < uniqueColors.length) {
      return uniqueColors[index];
    } else {
      // This generates a unique color incase the list of data exceed the available number of colors
      return HSLColor.fromAHSL(
        1.0,
        (index * 360 / uniqueColors.length) % 360,
        0.7,
        0.5,
      ).toColor();
    }
  }

  double _getMaxValue() {
    return data
            .map((e) => e['count'] as int)
            .reduce((a, b) => a > b ? a : b)
            .toDouble() *
        1.2;
  }
}
