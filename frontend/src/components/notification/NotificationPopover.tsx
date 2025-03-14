import React from "react";
import {
  Bell,
  X,
  TrendingUp,
  TrendingDown,
  Newspaper,
  BarChart2,
  AlertCircle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { ScrollArea } from "@/components/ui/scroll-area";

type NotificationTypeKey = 'PRICE_UP' | 'PRICE_DOWN' | 'NEWS' | 'MARKET' | 'ALERT';


interface Notification {
  id: number;
  type: NotificationTypeKey;
  title: string;
  message: string;
  time: string;
  read: boolean;
  actionUrl: string;
}

// Notification types with their specific icons and styles
const NOTIFICATION_TYPES = {
  PRICE_UP: {
    icon: TrendingUp,
    bgColor: "bg-green-50",
    iconColor: "text-green-600",
    borderColor: "border-l-green-500",
  },
  PRICE_DOWN: {
    icon: TrendingDown,
    bgColor: "bg-red-50",
    iconColor: "text-red-600",
    borderColor: "border-l-red-500",
  },
  NEWS: {
    icon: Newspaper,
    bgColor: "bg-blue-50",
    iconColor: "text-blue-600",
    borderColor: "border-l-blue-500",
  },
  MARKET: {
    icon: BarChart2,
    bgColor: "bg-purple-50",
    iconColor: "text-purple-600",
    borderColor: "border-l-purple-500",
  },
  ALERT: {
    icon: AlertCircle,
    bgColor: "bg-yellow-50",
    iconColor: "text-yellow-600",
    borderColor: "border-l-yellow-500",
  },
};

// Enhanced sample notifications with more variety and details
const SAMPLE_NOTIFICATIONS: Notification[] = [
  {
    id: 1,
    type: 'PRICE_UP',
    title: "AAPL Price Alert",
    message: "Apple stock is up 5.2% trading at $198.50",
    time: "5m ago",
    read: false,
    actionUrl: "/stocks/AAPL",
  },
  {
    id: 2,
    type: "NEWS",
    title: "Breaking News",
    message: "Tesla announces new factory location in Mexico",
    time: "15m ago",
    read: false,
    actionUrl: "/news/tesla-announcement",
  },
  {
    id: 3,
    type: "MARKET",
    title: "Market Update",
    message: "S&P 500 reaches new all-time high",
    time: "1h ago",
    read: false,
    actionUrl: "/market-overview",
  },
  {
    id: 4,
    type: "PRICE_DOWN",
    title: "NVDA Alert",
    message: "NVIDIA down 3.1% following sector-wide decline",
    time: "2h ago",
    read: true,
    actionUrl: "/stocks/NVDA",
  },
  {
    id: 5,
    type: "ALERT",
    title: "Watchlist Alert",
    message: "3 stocks in your watchlist are showing unusual volume",
    time: "3h ago",
    read: true,
    actionUrl: "/watchlist",
  },
];

export const NotificationPopover = () => {
  const [notifications, setNotifications] =
    React.useState(SAMPLE_NOTIFICATIONS);
  const unreadCount = notifications.filter((n) => !n.read).length;

const markAsRead = (id: number): void => {
    setNotifications(
        notifications.map((notification) =>
            notification.id === id ? { ...notification, read: true } : notification
        )
    );
};

  const markAllAsRead = () => {
    setNotifications(
      notifications.map((notification) => ({ ...notification, read: true }))
    );
  };

  const handleNotificationClick = (notification: Notification): void => {
    markAsRead(notification.id);
    // You can add navigation logic here using the actionUrl
    console.log("Navigate to:", notification.actionUrl);
  };

  return (
    <Popover>
      <PopoverTrigger asChild>
        <div className="relative">
          <Button variant="ghost" size="icon" className="relative">
            <Bell className="h-5 w-5" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-red-500 flex items-center justify-center">
                <span className="text-xs text-white font-medium">
                  {unreadCount}
                </span>
              </span>
            )}
          </Button>
        </div>
      </PopoverTrigger>
      <PopoverContent className="w-96 p-0" align="end">
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center gap-2">
            <Bell className="h-4 w-4 text-gray-500" />
            <span className="font-semibold">Notifications</span>
            {unreadCount > 0 && (
              <span className="bg-red-100 text-red-600 text-xs font-medium px-2 py-0.5 rounded-full">
                {unreadCount} new
              </span>
            )}
          </div>
          {unreadCount > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={markAllAsRead}
              className="text-sm text-blue-600 hover:text-blue-700 hover:bg-blue-50"
            >
              Mark all as read
            </Button>
          )}
        </div>
        <ScrollArea className="h-[400px]">
          {notifications.length > 0 ? (
            <div className="divide-y">
              {notifications.map((notification) => {
                const NotificationIcon =
                  NOTIFICATION_TYPES[notification.type].icon;
                return (
                  <div
                    key={notification.id}
                    onClick={() => handleNotificationClick(notification)}
                    className={`p-4 hover:bg-gray-50 transition-colors cursor-pointer border-l-4 ${
                      !notification.read
                        ? `${NOTIFICATION_TYPES[notification.type].bgColor} ${
                            NOTIFICATION_TYPES[notification.type].borderColor
                          }`
                        : "border-l-transparent"
                    }`}
                  >
                    <div className="flex gap-3">
                      <div
                        className={`mt-1 ${
                          NOTIFICATION_TYPES[notification.type].iconColor
                        }`}
                      >
                        <NotificationIcon className="h-5 w-5" />
                      </div>
                      <div className="flex-1 space-y-1">
                        <div className="flex justify-between items-start">
                          <p className="text-sm font-medium">
                            {notification.title}
                          </p>
                          {!notification.read && (
                            <Button
                              size="icon"
                              variant="ghost"
                              className="h-6 w-6 -mt-1 -mr-1"
                              onClick={(e) => {
                                e.stopPropagation();
                                markAsRead(notification.id);
                              }}
                            >
                              <X className="h-4 w-4" />
                            </Button>
                          )}
                        </div>
                        <p className="text-sm text-gray-600">
                          {notification.message}
                        </p>
                        <p className="text-xs text-gray-400">
                          {notification.time}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="p-8 text-center text-sm text-gray-500">
              No new notifications
            </div>
          )}
        </ScrollArea>
      </PopoverContent>
    </Popover>
  );
};

export default NotificationPopover;
