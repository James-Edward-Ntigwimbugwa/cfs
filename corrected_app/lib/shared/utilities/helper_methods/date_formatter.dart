import 'package:intl/intl.dart';

String customDateFormatter({required DateTime dateTime}) {
  return DateFormat("MMM dd yyyy, HH:mm").format(dateTime);
}
