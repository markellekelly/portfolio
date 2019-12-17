/* 
   Markelle Kelly and Lindsey Piggott
   CSC 365 Project A
*/

import java.sql.*;
import java.util.*;
import java.io.*;
import java.lang.*;
import java.text.*;
import java.math.*;
import java.util.ArrayList;

public class InnReservations {
  private static Connection conn = null;

  public static void main(String args[]) throws FileNotFoundException {
  try {
	  Class.forName("com.mysql.jdbc.Driver").newInstance();
  } catch (Exception ex) {
	  System.out.println("Driver not found");
	  System.out.println(ex);
  };
  String filename = "ServerSettings.txt";
  File file = new File(filename); 
  Scanner sc = new Scanner(file);
  String url = sc.nextLine().trim();
  String userID = sc.nextLine().trim();
  String pword = sc.nextLine().trim();
  try {
  	conn = DriverManager.getConnection(url, userID, pword);
  } catch (Exception ex) {
	 System.out.println("Could not open connection");
  };
  try {
    String createRooms = ("CREATE TABLE " + "IF NOT EXISTS " + 
        "myRooms LIKE INN.rooms");
    PreparedStatement stmtRo = conn.prepareStatement(createRooms); 
    stmtRo.executeUpdate();
    String createRes = ("CREATE TABLE " + "IF NOT EXISTS " +
        "myReservations LIKE INN.reservations");
    PreparedStatement stmtRe = conn.prepareStatement(createRes); 
    stmtRe.executeUpdate();
  } catch (Exception ex) {
    ex.printStackTrace();
  }
  boolean exit = false;
  Scanner input = new Scanner(System.in);
  // clear the screen to freshen up the display
  clearScreen();
  while (!exit) {
    displayMain();
	  char option = input.nextLine().toLowerCase().charAt(0);
	  switch(option) {
      case 'a':   adminLoop();
      break;
      case 'o':   ownerLoop();
      break;
      case 'g':   guestLoop();
      break;
      case 'q':   exit = true;
      break;
	  }
  }
  try {
    conn.close();
  } catch (Exception ex) {
  }
  input.close();
  }

  private static void displayMain() {
    // clearScreen();
    System.out.println("Welcome. Please choose your role:\n\n"
    + "- (A)dmin\n" + "- (O)wner\n" + "- (G)uest\n" + "- (Q)uit\n");
  }

  private static void adminLoop() {
    boolean exit = false;
    Scanner input = new Scanner(System.in);
    while (!exit) {
      displayAdmin();
      String[] tokens = input.nextLine().toLowerCase().split(" ");
      char option = tokens[0].charAt(0);
      System.out.println("option chosen: " + option);
      switch(option) {
        case 'v':   
          displayTable(tokens[1]);
          break;
        case 'c':   
          clearDB();
          break;
        case 'l':   
          loadDB();
          break;
        case 'r':   
          removeDB();
          break;
        case 'b':   
          exit = true;
          break;
      }
    }
   }

  private static void ownerLoop() {
    boolean exit = false;
    Scanner input = new Scanner(System.in);
    while (!exit) {
      displayOwner();
      String[] tokens = input.nextLine().toLowerCase().split("\\s");
      char option = tokens[0].charAt(0);
      char dataOpt = 0;
      if (tokens.length == 2) {
        dataOpt = tokens[1].charAt(0);
      }
      switch(option) {
        case 'o':   occupancyMenu();
                    break;
        case 'd':   dataMenu(dataOpt);
                    break;
        case 's':   browseRes();
                    break;
        case 'r':   browseRooms();
                    break;
        case 'b':   exit = true;
                    break;
      }
    }     
  }

  // Program loop for guest subsystem
  private static void guestLoop() {
    boolean exit = false;
    Scanner input = new Scanner(System.in);
    while (!exit) {
      displayGuest();
      char option = input.next().toLowerCase().charAt(0);
      switch(option) {
        case 'r':   
          roomsAndRates();
          break;
        case 's':
          viewStays();
          break;
        case 'b':   exit = true;
                    break;
      }
    }
  }

  // Guest UI display
  private static void displayGuest() {
    System.out.println("Welcome, Guest.\n\n"
      + "Choose an option:\n"
      + "- (R)ooms - View rooms and rates\n"
      + "- (S)tays - View availability for your stay\n"
      + "- (B)ack - Goes back to main menu\n");
  }

  // Admin UI display
  private static void displayAdmin() {
    String status;
    int rooms;
    int reservations;
    try {
      String query = "SELECT count(*) " + "FROM myRooms";
      PreparedStatement stmt = conn.prepareStatement(query); 
      ResultSet rset = stmt.executeQuery();
      rset.next();
      rooms = rset.getInt(1);
      String query2 = "SELECT count(*) " + "FROM myReservations";
      PreparedStatement stmt2 = conn.prepareStatement(query2); 
      ResultSet rset2 = stmt2.executeQuery();
      rset2.next();
      reservations = rset2.getInt(1);
      if (rooms > 0 && reservations > 0) {
        status = "full";
      } else {
        status = "empty";
      }
    } catch (Exception ex){
      status = "no database";
      rooms = 0;
      reservations = 0;
    }
    System.out.println("Welcome, Admin.\n\n"
        + "Current Status: " + status + "\n"
        + "Reservations: " + reservations + "\n"
        + "Rooms: " + rooms + "\n\n"
        + "Choose an option:\n"
        + "- (V)iew [table name] - Displays table contents\n"
        + "- (C)lear - Deletes all table contents\n"
        + "- (L)oad - Loads all table contents\n"
        + "- (R)emove - Removes tables\n"
        + "- (B)ack - Goes back to main menu\n");
  }

  // Owner UI display
  private static void displayOwner() {
    System.out.println("Welcome, Owner.\n\n"
      + "Choose an option:\n"
      + "- (O)ccupancy - View occupancy of rooms\n"
      + "- (D)ata [(c)ounts|(d)ays|(r)evenue] - View data on "
      + "counts, days, or revenue of each room\n"
      + "- (S)tays - Browse list of reservations\n"
      + "- (R)ooms - View list of rooms\n"
      + "- (B)ack - Goes back to main menu\n");
  }

  // Clears the console screen when running interactive
  private static void clearScreen() {
    Console c = System.console();
    if (c != null) {
      // Clear screen for the first time
      System.out.print("\033[H\033[2J");
      System.out.flush();
      //c.writer().print(ESC + "[2J");
      //c.flush();
      // Clear the screen again and place the cursor in the top left
      System.out.print("\033[H\033[1;1H");
      System.out.flush();
      //c.writer().print(ESC + "[1;1H");
      //c.flush();
    }
  }

  // ADMIN FUNCTIONS
  private static void displayTable(String table) {
    String roomsFormat = "| %-7s| %-25s| %-5s| %-8s| %-7s| %-10s| %-13s| %n";
    String resFormat = "| %-7s| %-6s| %-12s| %-12s| %-6s| %-15s| %-12s| %-8s| %-6s| %n";
    try {
      String tname = table.substring(0, 1).toUpperCase() + table.substring(1);
      String query = "SELECT * " + "FROM my" + tname;
      PreparedStatement stmt = conn.prepareStatement(query); 
      ResultSet rset = stmt.executeQuery();
      ResultSetMetaData rsmd = rset.getMetaData();
      int cols = rsmd.getColumnCount();
      if (tname.equals("Rooms")) {
        System.out.format(roomsFormat, "RoomId","RoomName","Beds","BedType","MaxOcc","BasePrice","Decor");
      } else if (tname.equals("Reservations")) {
        System.out.format(resFormat, "Code","Room","CheckIn","CheckOut","Rate","LastName","FirstName","Adults","Kids");
      }
      while (rset.next()) {
        String[] toPrint = new String[cols];
        for (int j=1; j<= cols; j++) {
          toPrint[j-1] = rset.getString(j);
        }
        if (tname.equals("Rooms")) {
          System.out.format(roomsFormat, toPrint[0],toPrint[1],toPrint[2],
            toPrint[3],toPrint[4],toPrint[5],toPrint[6]);
        } else if (tname.equals("Reservations")) {
          System.out.format(resFormat, toPrint[0],toPrint[1],toPrint[2],
            toPrint[3],toPrint[4],toPrint[5],toPrint[6],toPrint[7],toPrint[8]);
        }
      }
      System.out.println();System.out.println();
    } catch (Exception ex) {
      System.out.println("no table " + table);
    }
  }

  public static void clearDB() {
    try {
      String query1 = "DELETE FROM " + "myRooms";
      Statement stmt1 = conn.createStatement(); 
      stmt1.executeUpdate(query1);
    } catch (Exception ex) {
    }
    try {
      String query2 = "DELETE FROM " + "myReservations";
      Statement stmt2 = conn.createStatement(); 
      stmt2.executeUpdate(query2);
    } catch (Exception ex) {
    }
  }

  public static void loadDB() {
    try {
      String query = "SELECT count(*) " + "FROM myRooms";
      PreparedStatement stmt = conn.prepareStatement(query); 
      ResultSet rset = stmt.executeQuery();
      rset.next();
      int rooms = rset.getInt(1);
      String query2 = "SELECT count(*) " + "FROM myReservations";
      PreparedStatement stmt2 = conn.prepareStatement(query2); 
      ResultSet rset2 = stmt2.executeQuery();
      rset2.next();
      int reservations = rset2.getInt(1);
      if (rooms == 0 && reservations == 0) {
        String queryRo = "INSERT INTO " + "myRooms " +
          "(SELECT * FROM INN.rooms)";
        PreparedStatement stmtRo = conn.prepareStatement(queryRo); 
        stmtRo.executeUpdate();
        String queryRe = "INSERT INTO " + "myReservations " +
          "(SELECT * FROM INN.reservations)";
        PreparedStatement stmtRe = conn.prepareStatement(queryRe); 
        stmtRe.executeUpdate();
      } 
    } catch (Exception ex){
      try {
        String createRooms = ("CREATE TABLE " + "myRooms " + "AS " +
            "SELECT * FROM INN.rooms");
        PreparedStatement stmtRo = conn.prepareStatement(createRooms); 
        stmtRo.executeUpdate();
        String createRes = ("CREATE TABLE " + "myReservations " + "AS " +
            "SELECT * FROM INN.reservations");
        PreparedStatement stmtRe = conn.prepareStatement(createRes); 
        stmtRe.executeUpdate();
      } catch (Exception ex2){
        ex2.printStackTrace();
      }
    }  
  }

  public static void removeDB() {
    try {
      String removeRooms = "DROP TABLE myRooms";
      PreparedStatement rooms = conn.prepareStatement(removeRooms);
      rooms.executeUpdate();
      String removeRes = "DROP TABLE myReservations";
      PreparedStatement res = conn.prepareStatement(removeRes);
      res.executeUpdate();
    } catch (Exception ex){
    }
  }

  // OWNER FUNCTIONS
  private static void occupancyMenu() {
    boolean exit = false;
    Scanner input = new Scanner(System.in);
    while (!exit) {
      displayOccupancy();
      String[] tokens = input.nextLine().toLowerCase().split("\\s");
      char option = tokens[0].charAt(0);
      char dataOpt = 0;
      if (tokens.length == 2) {
        dataOpt = tokens[1].charAt(0);
      }
      switch(option) {
        case 'o':   enterDate();
                    break;
        case 't':   enterPeriod();
                    break;
        case 'b':   exit = true;
                    break;
      }
    }
  }

  private static void displayOccupancy() {
    System.out.println("Welcome, Owner.\n\n"
      + "Enter:\n"
      + "- (O)ne Date - View occupancy of rooms on date\n"
      + "- (T)wo Dates - View occupancy of rooms during time period\n"
      + "- (B)ack - Goes back to main menu\n"); 
  }

  private static void enterDate() {
    System.out.print("Date: ");
    try {
      String date = getDate();
      String query = "SELECT roomId " + "FROM myRooms";
      PreparedStatement stmt = conn.prepareStatement(query);
      ResultSet rset = stmt.executeQuery();
      System.out.println();
      System.out.println("Room Status");
      while (rset.next ()){
        String q = "SELECT * " + "FROM myRooms r, myReservations re" +
                   " WHERE re.CheckIn <= " +  
                   "STR_TO_DATE(" + date + ",'%Y-%m-%d') AND re.CheckOut > " + 
                   "STR_TO_DATE(" + date + ",'%Y-%m-%d')" + 
                   " AND r.roomId = re.room AND r.roomId = \"" + rset.getString(1) + "\"";
        PreparedStatement s = conn.prepareStatement(q);
        ResultSet r = s.executeQuery();
        System.out.print(rset.getString("RoomId"));
        if (r.next()) {
           System.out.println("  Occupied");
        } else {
           System.out.println("  Empty");
        }
        r.close();
      }
      rset.close();
      System.out.println();
      String roomCode = getRoomCodeOrQ();
      if (roomCode.toLowerCase().charAt(0) != 'q') {
        String fullFormat = "| %-7s| %-6s| %-25s| %-12s| %-12s| %-6s| %-15s| %-12s| %-8s| %-6s| %n";
        String select = "SELECT * FROM myReservations "
          + "WHERE Room = \"" + roomCode + "\" AND CheckIn <= " +  
          "STR_TO_DATE(" + date + ",'%Y-%m-%d') AND CheckOut > " + 
          "STR_TO_DATE(" + date + ",'%Y-%m-%d')";
        PreparedStatement stm = conn.prepareStatement(select);
        ResultSet rs = stm.executeQuery();
        String getRoomName = "SELECT RoomName FROM myRooms WHERE RoomId = \""
            + roomCode.toUpperCase() + "\"";
        PreparedStatement sewa = conn.prepareStatement(getRoomName);
        ResultSet gettinName = sewa.executeQuery();
        gettinName.next();
        String roomName = gettinName.getString(1);
        if (rs.next()) {
          System.out.format(fullFormat, "Code","Room","RoomName","CheckIn","CheckOut","Rate","LastName","FirstName","Adults","Kids");
          System.out.format(fullFormat, rs.getInt(1), rs.getString(2), roomName, rs.getString(3),
            rs.getString(4), rs.getInt(5), rs.getString(6), rs.getString(7), 
            rs.getInt(8), rs.getInt(9));
        }
      }
      System.out.println();
    } catch (SQLException ex) {
    }
  }

  private static void enterPeriod() {
    try {
      String[] dates = getDatesFull();
      String query = "SELECT roomId " + "FROM myRooms";
      PreparedStatement stmt = conn.prepareStatement(query);
      ResultSet rset = stmt.executeQuery();
      while (rset.next()) {
        boolean someOcc = false;
        boolean someVac = false;
        for (String date : dates) {
          String q = "SELECT r.roomName " + "FROM myRooms r, myReservations re " +
            "WHERE r.RoomId = re.Room " + "AND re.CheckIn <= " +  "STR_TO_DATE(\"" +
            date + "\",'%Y-%m-%d')" + "AND re.CheckOut > " + "STR_TO_DATE(\"" + date +
            "\",'%Y-%m-%d')" + " AND r.roomId = \"" + rset.getString(1) + "\"";
          PreparedStatement s = conn.prepareStatement(q);
          ResultSet r = s.executeQuery();
          if (r.next()) {
            someOcc = true;
          } else {
            someVac = true;
          }
          r.close();
          if (someOcc && someVac) {
            break;
          }
        }
        System.out.print(rset.getString("RoomId"));
        if (someOcc && someVac) {
          System.out.println("  Partially occupied");
        } else if (someOcc) {
          System.out.println("  Fully occupied");
        } else {
          System.out.println("  Fully vacant");
        }
      }
      rset.close();
      String reservations = getRoomCodeOrQ();
      if (reservations.toLowerCase().charAt(0) != 'q') {
        String resv = "SELECT Code, CheckIn, CheckOut FROM myReservations"
          + " WHERE Room = \"" + reservations + "\" AND ((CheckIn < STR_TO_DATE(\"" 
          + dates[0] + "\",'%Y-%m-%d') AND CheckOut > STR_TO_DATE(\"" + dates[0] 
          + "\",'%Y-%m-%d')) OR " + "(CheckIn >= STR_TO_DATE(\"" + dates[0] + 
          "\",'%Y-%m-%d') AND CheckIn <= STR_TO_DATE(\"" + dates[dates.length - 1] + 
          "\",'%Y-%m-%d')))";
        PreparedStatement stmtt = conn.prepareStatement(resv);
        ResultSet rest = stmtt.executeQuery();
        String resFormat = "| %-7s| %-12s| %-12s| %n";
        if (rest.next()) {
          System.out.format(resFormat, "Code", "CheckIn", "CheckOut");
          System.out.format(resFormat, rest.getInt(1), rest.getString(2), 
            rest.getString(3));
        }
        while (rest.next()) {
          System.out.format(resFormat, rest.getInt(1), rest.getString(2), 
            rest.getString(3));
        }
        System.out.println();
        String reserveCode = getReservCodeOrQ();
        if (reserveCode.toLowerCase().charAt(0) != 'q') {
          String fullFormat = "| %-7s| %-6s| %-25s| %-12s| %-12s| %-6s| %-15s| %-12s| %-8s| %-6s| %n";
          String select = "SELECT * FROM myReservations "
            + "WHERE Code = \"" + reserveCode + "\"";
          PreparedStatement stm = conn.prepareStatement(select);
          ResultSet rs = stm.executeQuery();
          String getRoomName = "SELECT RoomName FROM myRooms WHERE RoomId = \""
            + reservations.toUpperCase() + "\"";
          PreparedStatement sewa = conn.prepareStatement(getRoomName);
          ResultSet gettinName = sewa.executeQuery();
          gettinName.next();
          String roomName = gettinName.getString(1);
          rs.next();
          System.out.format(fullFormat, "Code","Room","RoomName","CheckIn","CheckOut","Rate","LastName","FirstName","Adults","Kids");
          System.out.format(fullFormat, rs.getInt(1), rs.getString(2), roomName, rs.getString(3),
            rs.getString(4), rs.getInt(5), rs.getString(6), rs.getString(7), 
            rs.getInt(8), rs.getInt(9));
        }
        System.out.println();
      }
    } catch (SQLException ex) {
      ex.printStackTrace();
    }
  }

  public static String[] getDatesFull() {
    ArrayList<String> dates = new ArrayList<String>();
    int[] months30 = new int[] {4, 6, 9, 11};
    System.out.print("Enter start date: ");
    Scanner input = new Scanner(System.in);
    String monthName = input.next();
    int startMonth = monthNum(monthName);
    int startDay = input.nextInt();
    System.out.print("Enter end date: ");
    String month = input.next();
    int endMonth = monthNum(month);
    int endDay = input.nextInt();
    while (endDay != startDay || endMonth != startMonth) {
      dates.add("2010-" + startMonth + "-" + startDay);
      if (startMonth == 2 && startDay == 28){
        startMonth++;
        startDay = 1;
      } else if ((startDay == 30 && contains(months30, startMonth)) || startDay == 31){
        startMonth++;
        startDay = 1;
      } else {
        startDay++;
      }
    }
    dates.add("2010-" + endMonth + "-" + endDay);
    return dates.toArray(new String[dates.size()]);
  }

  private static void dataMenu(char type) {
    while (type == 'c' || type == 'd' || type == 'r') {
      try {
        String getRooms = "SELECT * FROM myRooms";
        PreparedStatement roomsSt = conn.prepareStatement(getRooms);
        ResultSet rooms = roomsSt.executeQuery();
        ArrayList<String[]> data = new ArrayList<String[]>();
        int[] totals = new int[13];
        while (rooms.next()) {
          String[] byMonth = new String[13];
          int sum = 0;
          String getInfo = "SELECT ";
          switch(type) {
            case 'c': 
              getInfo = getInfo + "count(*) ";
              break;
            case 'd':
              getInfo = getInfo + "sum(DATEDIFF(CheckOut, CheckIn)) ";
              break;
            case 'r':
              getInfo = getInfo + "sum(DATEDIFF(CheckOut, CheckIn)*Rate) ";
              break;
          }
          getInfo = getInfo + "FROM myReservations " + "WHERE Room = \"" 
              + rooms.getString(1) + "\" GROUP BY MONTH(CheckOut)";
          PreparedStatement cSt = conn.prepareStatement(getInfo);
          ResultSet cR = cSt.executeQuery();
          int i = 1;
          while (i<=12) {
            cR.next();
            byMonth[i-1] = cR.getString(1);
            totals[i-1] = totals[i-1] + cR.getInt(1);
            sum = sum + cR.getInt(1);
            i++;
          }
          byMonth[12] = ""+ sum;
          totals[12] = totals[12] + sum;
          data.add(byMonth);
        }
        System.out.println();
        switch(type) {
            case 'c': 
              System.out.println("Number of Reservations");
              break;
            case 'd':
              System.out.println("Total Days Occupied");
              break;
            case 'r':
              System.out.println("Revenue ($)");
              break;
          }
        String revFormat = "| %-5s | %-5s | %-5s | %-5s | %-5s | %-5s | %-5s |" + 
          " %-5s | %-5s | %-5s | %-5s | %-5s | %-5s | %-6s | %n";
        rooms.beforeFirst();
        int j=0;
        System.out.format(revFormat, "Room","Jan","Feb","Mar","Apr","May",
          "Jun","Jul","Aug","Sep","Oct","Nov","Dec","Total");
        while (rooms.next()) {
          System.out.format(revFormat,rooms.getString(1),data.get(j)[0],data.get(j)[1],
            data.get(j)[2],data.get(j)[3],data.get(j)[4],data.get(j)[5],data.get(j)[6],
            data.get(j)[7],data.get(j)[8],data.get(j)[9],data.get(j)[10],data.get(j)[11],
            data.get(j)[12]);
          j++;
        }
        System.out.format(revFormat,"Total",totals[0],totals[1],totals[2],totals[3],
          totals[4],totals[5],totals[6],totals[7],totals[8],totals[9],totals[10],
          totals[11],totals[12]);
        System.out.println();
      } catch (Exception ex) {
        ex.printStackTrace();
      }
       type = revenueData();
    }
    System.out.println();
  }

  private static void browseRes() {
    System.out.print("Would you like to enter a range of dates? (y)es or (n)o: ");
    Scanner input = new Scanner(System.in);
    String dates = input.next();
    String startDate = null; String endDate = null;
    if (dates.toLowerCase().charAt(0) == 'y') {
      System.out.print("\nEnter start date: ");
      String monthName = input.next();
      int startMonth = monthNum(monthName);
      int startDay = input.nextInt();
      startDate = "2010-" + startMonth + "-" + startDay;
      System.out.print("\nEnter end date: ");
      String month = input.next();
      int endMonth = monthNum(month);
      int endDay = input.nextInt();
      endDate = "2010-" + endMonth + "-" + endDay;
    }
    System.out.print("\nWould you like to view a specific room? (y)es or (n)o: ");
    String room = input.next();
    String roomCode = null;
    if (room.toLowerCase().charAt(0) == 'y') {
      System.out.print("\nEnter room code: ");
      roomCode = input.next();
    }
    String query = "SELECT Code, Room, CheckIn, CheckOut FROM myReservations";
    boolean needAnd = false;
    if (dates.toLowerCase().charAt(0) == 'y') {
      query = query + " WHERE CheckIn >= STR_TO_DATE(\""+ startDate + "\",'%Y-%m-%d') AND " 
          + " CheckIn <= STR_TO_DATE(\"" + endDate + "\",'%Y-%m-%d')";
      needAnd = true;
    } 
    if (room.toLowerCase().charAt(0) == 'y') {
      if (needAnd) {
        query = query + " AND";
      } else {
        query = query + " WHERE";
      }
      query = query + " Room = \"" + roomCode + "\"";
    }
    try {
      PreparedStatement stmt = conn.prepareStatement(query);
      ResultSet rset = stmt.executeQuery();
      String resFormat = "| %-7s| %-6s| %-12s| %-12s| %n";
      if (rset.next()) {
        System.out.format(resFormat, "Code", "Room", "CheckIn", "CheckOut");
        System.out.format(resFormat, rset.getInt(1), rset.getString(2), 
          rset.getString(3), rset.getString(4));
      }
      while (rset.next()) {
        System.out.format(resFormat, rset.getInt(1), rset.getString(2), 
          rset.getString(3), rset.getString(4));
      }
      System.out.println();
      String reserveCode = getReservCodeOrQ();
      if (reserveCode.toLowerCase().charAt(0) != 'q') {
        String fullFormat = "| %-7s| %-6s| %-25s| %-12s| %-12s| %-6s| %-15s| %-12s| %-8s| %-6s| %n";
        String select = "SELECT * FROM myReservations "
          + "WHERE Code = \"" + reserveCode + "\"";
        PreparedStatement stm = conn.prepareStatement(select);
        ResultSet rs = stm.executeQuery();
        if (roomCode == null) {
          String getRoomCode = "SELECT Room FROM myReservations WHERE Code = "
            + reserveCode;
          PreparedStatement awef = conn.prepareStatement(getRoomCode);
          ResultSet waw = awef.executeQuery();
          if (waw.next()) {
            roomCode = waw.getString(1);
          }
        }
        String getRoomName = "SELECT RoomName FROM myRooms WHERE RoomId = \""
            + roomCode.toUpperCase() + "\"";
        PreparedStatement sewa = conn.prepareStatement(getRoomName);
        ResultSet gettinName = sewa.executeQuery();
        gettinName.next();
        String roomName = gettinName.getString(1);
        rs.next();
        System.out.format(fullFormat, "Code","Room","RoomName","CheckIn","CheckOut",
          "Rate","LastName","FirstName","Adults","Kids");
        System.out.format(fullFormat, rs.getInt(1), rs.getString(2), roomName,
          rs.getString(3), rs.getString(4), rs.getInt(5), rs.getString(6),
          rs.getString(7), rs.getInt(8), rs.getInt(9));
      }
      System.out.println();
    } catch (Exception ex) {
      ex.printStackTrace();
    }
  }

  private static void browseRooms() {
    try {
      String query = "SELECT * " + "FROM myRooms";
      PreparedStatement stmt = conn.prepareStatement(query); 
      ResultSet rset = stmt.executeQuery();
      System.out.println();
      System.out.println("RoomId\tRoomName");
      while (rset.next()) {
        System.out.print(rset.getString("RoomId"));
        System.out.println("\t" + rset.getString("RoomName"));
      }
      System.out.println();
      String view = viewRooms();
      String roomCode = "";
      if (view.charAt(0) != 'q') {
        roomCode = view.split(" ")[1];
      }
      while (view.charAt(0) == 'v') {
        String select = "SELECT * " + "FROM myRooms r " + 
          "WHERE r.RoomId = " + roomCode.toUpperCase();
        PreparedStatement sstmt = conn.prepareStatement(select); 
        ResultSet room = sstmt.executeQuery();
        String totalRev = "SELECT sum(DATEDIFF(CheckOut,CheckIn)*Rate) " +
          "FROM myReservations";
        PreparedStatement rStmt= conn.prepareStatement(totalRev);
        ResultSet allRev = rStmt.executeQuery();
        allRev.next();
        int totalRevenue = allRev.getInt(1);
        String info = "SELECT sum(DATEDIFF(CheckOut,CheckIn)), " +
          "sum(DATEDIFF(CheckOut, CheckIn) * Rate) FROM myReservations " +
          "WHERE Room = " + roomCode.toUpperCase();
        PreparedStatement iSt= conn.prepareStatement(info);
        ResultSet iRes = iSt.executeQuery();
        iRes.next();
        int nightsOcc = iRes.getInt(1);
        double percentOccu = ((double) nightsOcc / (double) 365) * (double) 100;
        double percentOcc = Math.round(percentOccu * 100.0) / 100.0;
        int revenue = iRes.getInt(2);
        double percentRevu = ((double) revenue / (double) totalRevenue) * (double) 100;
        double percentRev = Math.round(percentRevu * 100.0) / 100.0;
        String roomsFormat = "| %-7s| %-25s| %-5s| %-8s| %-7s| %-10s| %-13s|" + 
          " %-10s| %-7s| %-8s| %-9s| %n";
        System.out.format(roomsFormat, "RoomId","RoomName","Beds","BedType",
            "MaxOcc","BasePrice","Decor", "NightsOcc", "%Occ", "Revenue", "%Revenue");
        room.next();
        System.out.format(roomsFormat,room.getString(1),room.getString(2),
          room.getInt(3),room.getString(4),room.getInt(5),room.getInt(6),
          room.getString(7), nightsOcc, percentOcc, revenue, percentRev);
        System.out.println();
        view = viewRooms();
      }
      if (view.charAt(0) == 'r') {
        String select = "SELECT Code, CheckIn, CheckOut FROM myReservations " +
          "WHERE Room = " + roomCode.toUpperCase() + " ORDER BY CheckIn";
        PreparedStatement rstmt = conn.prepareStatement(select);
        ResultSet rrset = rstmt.executeQuery();
        System.out.println();
        String resFormat = "| %-7s| %-12s| %-12s| %n";
        System.out.format(resFormat, "Code", "CheckIn", "CheckOut");
        while (rrset.next()) {
          System.out.format(resFormat, rrset.getInt(1), rrset.getString(2), 
            rrset.getString(3));
        }
        System.out.println();
        String reserveCode = getReservCodeOrQ();
        while (reserveCode.toLowerCase().charAt(0) != 'q') {
          String fullFormat = "| %-7s| %-6s| %-25s| %-12s| %-12s| %-6s| %-15s| %-12s| %-8s| %-6s| %n";
          String selecto = "SELECT * FROM myReservations "
            + "WHERE Code = \"" + reserveCode + "\"";
          PreparedStatement stm = conn.prepareStatement(selecto);
          ResultSet rs = stm.executeQuery();
          String getRoomName = "SELECT RoomName FROM myRooms WHERE RoomId = "
            + roomCode.toUpperCase();
          PreparedStatement sewa = conn.prepareStatement(getRoomName);
          ResultSet gettinName = sewa.executeQuery();
          gettinName.next();
          String roomName = gettinName.getString(1);
          rs.next();
          System.out.format(fullFormat, "Code","Room","RoomName","CheckIn","CheckOut","Rate","LastName","FirstName","Adults","Kids");
          System.out.format(fullFormat, rs.getInt(1), rs.getString(2), roomName, rs.getString(3),
            rs.getString(4), rs.getInt(5), rs.getString(6), rs.getString(7), 
            rs.getInt(8), rs.getInt(9));
          System.out.println();
          reserveCode = getReservCodeOrQ();
        }
      }
      System.out.println();
    } catch (Exception ex) {
      ex.printStackTrace();
    }
  }

  // GUEST FUNCTIONS
  public static void roomsAndRates() {
    try {
      String query = "SELECT * " + "FROM myRooms";
      PreparedStatement stmt = conn.prepareStatement(query); 
      ResultSet rset = stmt.executeQuery();
      System.out.println("RoomId\tRoomName");
      while (rset.next()) {
        System.out.print(rset.getString("RoomId"));
        System.out.println("\t" + rset.getString("RoomName"));
      }
      System.out.println();
      String roomCode = getRoomCodeOrQ();
      char quit = roomCode.toLowerCase().charAt(0);
      if (quit != 'q') {
        String select = "SELECT * " + "FROM myRooms r " + 
          "WHERE r.RoomId = \"" + roomCode.toUpperCase() + "\"";
        PreparedStatement sstmt = conn.prepareStatement(select); 
        ResultSet room = sstmt.executeQuery();
        String roomsFormat = "| %-7s| %-25s| %-5s| %-8s| %-7s| %-10s| %-13s| %n";
        String[] toPrint = null;
        while (room.next()) {
          toPrint = new String[7];
          for (int j=1; j<= 7; j++) {
            toPrint[j-1] = room.getString(j);
          }
        }
        if (toPrint != null) {
          System.out.format(roomsFormat, "RoomId","RoomName","Beds","BedType",
            "MaxOcc","BasePrice","Decor");
          System.out.format(roomsFormat, toPrint[0],toPrint[1],toPrint[2],
            toPrint[3],toPrint[4],toPrint[5],toPrint[6]);
          System.out.println();
          char c = availabilityOrGoBack();
          if (c == 'a') {
            viewAvailability(roomCode);
          }
        }
      } 
    } catch (Exception ex) {
      ex.printStackTrace();
    }
  }

  public static void viewAvailability(String roomCode) {
    String[] dates = getDates();
    boolean available = true;
    ArrayList<String> newDates = new ArrayList<String>();
    for (String date: dates) {
      try {
        String select = "SELECT * " + "FROM myRooms r, myReservations re " + 
          "WHERE (r.RoomId = \"" + roomCode.toUpperCase() + "\" "
          + "AND r.RoomId = re.Room " + "AND re.CheckIn <= " +
          "STR_TO_DATE(\"" + date + "\",'%Y-%m-%d') AND re.CheckOut > " + 
          "STR_TO_DATE(\"" + date + "\",'%Y-%m-%d'))";
        PreparedStatement stmt = conn.prepareStatement(select); 
        ResultSet rset = stmt.executeQuery();
        if (rset.next()) {
          available = false;
        } else {
          newDates.add(date);
        }
      } catch (Exception ex) {
        ex.printStackTrace();
      }
    }
    String avFormat = "| %-9s | %-9s| %n";
    String[] avDates = new String[newDates.size()];
    avDates = newDates.toArray(avDates);
    double rate = getPrice(roomCode, avDates);
    System.out.format(avFormat, "Date", "Rate");
    for (String date: dates) {
      if (contains(newDates, date)) {
        System.out.format(avFormat, date, rate);
      } else {
        System.out.format(avFormat, date, "Occupied");
      }
    }
    System.out.println();
    if (available) {
      char reserve = reserveOrGoBack();
      if (reserve == 'r') {
        placeReservation(dates[0],dates[dates.length -1], roomCode, rate);
      } else {
        System.out.println();
      }
    }
  }
  public static String[] getDates() {
    ArrayList<String> dates = new ArrayList<String>();
    int[] months30 = new int[] {4, 6, 9, 11};
    System.out.print("Enter check in date: ");
    Scanner input = new Scanner(System.in);
    String monthName = input.next();
    int startMonth = monthNum(monthName);
    int startDay = input.nextInt();
    System.out.print("Enter check out date: ");
    String month = input.next();
    int endMonth = monthNum(month);
    int endDay = input.nextInt();
    while (endDay != startDay || endMonth != startMonth) {
      dates.add("2010-" + startMonth + "-" + startDay);
      if (startMonth == 2 && startDay == 28){
        startMonth++;
        startDay = 1;
      } else if ((startDay == 30 && contains(months30, startMonth)) || startDay == 31){
        startMonth++;
        startDay = 1;
      } else {
        startDay++;
      }
    }
    return dates.toArray(new String[dates.size()]);
  }
  public static boolean contains(int[] array, int key) {
    for (int i : array) {
      if (i == key) {
        return true;
      }
    }
    return false;
  }
  public static boolean contains(ArrayList<String> array, String key) {
    for (String s : array) {
      if (s.equals(key)) {
        return true;
      }
    }
    return false;
  }
  public static double getPrice(String roomCode, String[] dates) {
    double baseRate = 0;
    try {
      String rate = "SELECT r.BasePrice FROM myRooms r " + "WHERE r.RoomId = \""
        + roomCode + "\"";
      PreparedStatement stm = conn.prepareStatement(rate);
      ResultSet result = stm.executeQuery();
      if (result.next()) {
        baseRate = result.getInt(1);
      }
    } catch (Exception ex) {
    }
    boolean holiday = false;
    boolean weekend = false;
    for (String date: dates) {
      String[] splitDate = date.split("-");
      if ((splitDate[1].equals("1") && splitDate[2].equals("1")) || 
      (splitDate[1].equals("7") && splitDate[2].equals("4")) ||
      (splitDate[1].equals("9")&& splitDate[2].equals("6")||
      splitDate[1].equals("10") && splitDate[2].equals("30"))) {
        holiday = true;
      }
      if (!holiday) {
        try {
          String query = "SELECT WEEKDAY(STR_TO_DATE(\"" +
            date + "\",\"%Y-%m-%d\")) FROM DUAL"; 
          PreparedStatement stmt = conn.prepareStatement(query); 
          ResultSet rset = stmt.executeQuery();
          if (rset.next()) {
            if (rset.getInt(1) == 5 || rset.getInt(1) == 6) {
              weekend =true;
            }
          }
        } catch (Exception ex) {
        }
      }
    }
    if (holiday) {
      baseRate = baseRate * 1.25;
    } else if (weekend) {
      baseRate = baseRate * 1.1;
    }
    double roundOff = Math.round(baseRate * 100.0) / 100.0;
    return roundOff;
  }

  public static void viewStays() {
    String[] dates = getDates();
    String roomFormat = "| %4s | %-25s| %-6s| %n";
    try {
      String rooms = "SELECT DISTINCT r.RoomId " + "FROM myRooms r";
      PreparedStatement stm = conn.prepareStatement(rooms); 
      ResultSet res = stm.executeQuery();
      ArrayList<String> available = new ArrayList<String>();
      while (res.next()) {
        available.add(res.getString(1));
      }
      for (String date: dates) {
        ArrayList<String> stillAvailable = new ArrayList<String>();
        String select = "SELECT DISTINCT r.RoomId " + 
          "FROM myRooms r, myReservations re " + 
          "WHERE (r.RoomId = re.Room " + "AND re.CheckIn <= " +
          "STR_TO_DATE(\"" + date + "\",'%Y-%m-%d') AND re.CheckOut > " + 
          "STR_TO_DATE(\"" + date + "\",'%Y-%m-%d'))";
        PreparedStatement stmt = conn.prepareStatement(select); 
        ResultSet rset = stmt.executeQuery();
        while (rset.next()) {
          stillAvailable.add(rset.getString(1));
        }
        ArrayList<String> toRemove = new ArrayList<String>();
        for (String code : available) {
          if (!contains(stillAvailable, code)) {
            toRemove.add(code);
          }
        }
        for (String code : toRemove){
          available.remove(code);
        }
      }
      if (available.size() > 0) {
        System.out.format(roomFormat, "Code", "Room Name", "Rate");
      }
      for (String code : available) {
        double rate = getPrice(code, dates);
        String getName = "SELECT r.RoomName FROM myRooms r " +
          "WHERE r.RoomId = \"" + code + "\"";
        PreparedStatement name = conn.prepareStatement(getName);
        ResultSet roomName = name.executeQuery();
        roomName.next();
        System.out.format(roomFormat, code, roomName.getString(1), rate);
      }
      System.out.println();
      if (available.size() > 0) {
      String cont = getRoomCodeOrQ();
        if (cont.charAt(0) != 'q') {
          String select = "SELECT * " + "FROM myRooms r " + 
            "WHERE r.RoomId = \"" + cont.toUpperCase() + "\"";
          PreparedStatement sstmt = conn.prepareStatement(select); 
          ResultSet room = sstmt.executeQuery();
          String roomsFormat = "| %-7s| %-25s| %-5s| %-8s| %-7s| %-10s| %-13s| %n";
          String[] toPrint = null;
          while (room.next()) {
            toPrint = new String[7];
            for (int j=1; j<= 7; j++) {
              toPrint[j-1] = room.getString(j);
            }
          }
          if (toPrint != null) {
            System.out.format(roomsFormat, "RoomId","RoomName","Beds","BedType",
              "MaxOcc","BasePrice","Decor");
            System.out.format(roomsFormat, toPrint[0],toPrint[1],toPrint[2],
              toPrint[3],toPrint[4],toPrint[5],toPrint[6]);
            System.out.println();
            char reserve = reserveOrGoBack();
            if (reserve == 'r') {
              placeReservation(dates[0], dates[dates.length -1], cont, getPrice(cont, dates));
            }
          }
        }
      }
    } catch (Exception ex) {
      ex.printStackTrace();
    }
  }

  private static void placeReservation(String startDate, String endDate, String roomCode, double rate) {
    try {
      String firstName = getFirstName();
      String lastName = getLastName();
      String select = "SELECT MaxOcc " + "FROM myRooms " + 
            "WHERE RoomId = \"" + roomCode + "\"";
      PreparedStatement sstmt = conn.prepareStatement(select); 
      ResultSet occ = sstmt.executeQuery();
      occ.next();
      int capacity = occ.getInt(1);
      int adults = getNumAdults();
      while (adults > capacity) {
        System.out.println("Sorry, the capacity for this room is " + capacity + ".");
        adults = getNumAdults();
      }
      int children = getNumChildren();
      while ((children + adults) > capacity) {
        System.out.println("Sorry, the capacity for this room is " + capacity + ".");
        adults = getNumAdults();
        children = getNumChildren();
      }
      String discount = getDiscount();
      if (discount.equals("AAA")) {
        rate = rate - rate*.1;
      } else if (discount.equals("AARP")) {
        rate = rate - rate*.15;
      }
      String fName = firstName.replace("'", "");
      String lName = lastName.replace("'", "");
      int newRate = (int) Math.round(rate);
      System.out.print("Would you like to place this reservation for " + fName +
        " " + lName + ", starting on " + startDate + ", at a rate of $" + newRate 
        + " per night? Enter (y)es to confirm, or (n)o to exit: ");
      Scanner input = new Scanner(System.in);
      String response = input.next();
      if (response.toLowerCase().charAt(0) == 'y') {
        confirmReservation(roomCode, startDate, endDate, newRate, lastName, firstName,
          adults, children);
      } 
      System.out.println();
    } catch (Exception ex) {
      ex.printStackTrace();
    }
  }
  private static void confirmReservation(String roomCode, String startDate, String endDate,
  int rate, String lastName, String firstName, int adults, int children) {
    try {
      String query = "SELECT max(Code) FROM myReservations";
      PreparedStatement stmt = conn.prepareStatement(query);
      ResultSet rset = stmt.executeQuery();
      rset.next();
      int oldId = rset.getInt(1);
      int newId = oldId + 1;
      if (newId > 99999) {
        boolean goodId = false;
        while (!goodId) {
          newId= oldId -1;
          String check = "SELECT * FROM myReservations " + "WHERE Code = " + newId;
          PreparedStatement cstmt = conn.prepareStatement(check);
          ResultSet crset = cstmt.executeQuery();
          if (crset.next()) {
            newId--;
          } else {
            goodId = true;
          }
        }
      }
      int[] months30 = new int[] {4, 6, 9, 11};
      String[] dateParts = endDate.split("-");
      int month = Integer.parseInt(dateParts[1]);
      int day = Integer.parseInt(dateParts[2]);
      if ((month == 2 && day == 28) || (contains(months30, month) && day == 30) 
        || day == 31) {
        day = 1;
        month++;
      } else {
        day++;
      }
      String newDate = "2010-" + month + "-" + day;
      String update = "INSERT INTO myReservations VALUES(" + newId + ", \"" + roomCode
        + "\", STR_TO_DATE(\"" + startDate + "\",'%Y-%m-%d'), STR_TO_DATE(\"" + newDate + 
        "\",'%Y-%m-%d'), " + rate + ", " + lastName + ", " + firstName + ", " 
        + adults + ", " + children + ")";
      PreparedStatement ustmt = conn.prepareStatement(update);
      ustmt.executeUpdate();
      String fName = firstName.replace("'", "");
      String lName = lastName.replace("'", "");
      System.out.println("Your reservation is complete.");
      System.out.println("\tName: " + fName + " "+ lName);
      System.out.println("\tRoom: " + roomCode + " at $" + rate + " per night");
      System.out.println("\tFrom: " + startDate);
      System.out.println("\tTo: " + newDate);
      String guests = "For ";
      if (adults == 1) {
        guests = guests + "1 adult";
      } else {
        guests = guests + adults + " adults";
      }
      if (children != 0) {
        if (children == 1) {
          guests = guests + " and 1 child";
        } else {
          guests = guests + " and " + children + "children";
        }
      }
      System.out.println("\t" + guests);
      System.out.println("Your reservation code is " + newId + ".");
    } catch (Exception ex) {
      ex.printStackTrace();
    }
  }

  // Get a date from input
  private static String getDate() {
    Scanner input = new Scanner(System.in);
    String monthName = input.next();
    int month = monthNum(monthName);
    int day = input.nextInt();
    String date = "'2010-" + month + "-" + day + "'";
    return date;
  }

  // Convert month name to month number
  private static int monthNum(String month) {
    switch (month) {
      case "january": return 1;
      case "february": return 2;
      case "march": return 3;
      case "april": return 4;
      case "may": return 5;
      case "june": return 6;
      case "july": return 7;
      case "august": return 8;
      case "september": return 9;
      case "october": return 10;
      case "november": return 11;
      case "december": return 12;
    }
    return 0;
  }
 
  // ask how many dates will be entered
  private static int getNumDates() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter number of dates (1 or 2): ");
    int numDates = input.nextInt();
    while (numDates != 1 && numDates != 2) {
        System.out.print("Enter number of dates (1 or 2): ");
        numDates = input.nextInt();
    }
    return numDates;
  }

  // get the room code or a 'q' response to back up the menu
  private static String getRoomCodeOrQ() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter room code for more details "
      + "(or (q)uit to exit): ");
    String roomCode = input.next();
    return roomCode;
  }

  // get the reservation code or a 'q' response to back up the menu
  private static String getReservCodeOrQ() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter reservation code for more details "
      + "(or (q)uit to exit): ");
    String rvCode = input.next();
    return rvCode;
  }

  // Revenue and volume data subsystem -- option to continue or quit
  private static char revenueData() {
    Scanner input = new Scanner(System.in);
    char opt;
    System.out.print("Type (c)ount, (d)ays, or (r)evenue to view "
      + "different table data (or (q)uit to exit): ");
    opt = input.next().toLowerCase().charAt(0);
    return opt;
  }

  // potentially useful for Rooms Viewing Subsystem -- gets option to
  // view room code or reservations room code or exit
  private static String viewRooms() {
    Scanner input = new Scanner(System.in);
    System.out.print("Type (v)iew [room code] or "
      + "(r)eservations [room code], or (q)uit to exit: ");
    char option = input.next().toLowerCase().charAt(0);
    String roomCode = String.valueOf(option);
    if (option != 'q') {
      roomCode = roomCode + " '" + input.next() + "'";
    }
    return roomCode;
  }

  // ask user if they wish to quit
  private static char askIfQuit() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter (q)uit to quit: ");
    char go = input.next().toLowerCase().charAt(0);
    return go;
  }

  // ask user if they wish to go back
  private static char askIfGoBack() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter (b)ack to go back: ");
    char go = input.next().toLowerCase().charAt(0);
    return go;
  }

  // potentially useful for check availability subsystem
  private static char availabilityOrGoBack() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter (a)vailability, or "
      + "(b)ack to go back: ");
    char option = input.next().toLowerCase().charAt(0);
    return option;
  }

  // Check availability subsystem:
  // ask if they want to place reservation or renege
  private static char reserveOrGoBack() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter (r)eserve to place a reservation, "
      + "or (b)ack to go back: ");
    char option = input.next().toLowerCase().charAt(0);
    return option;
  }

  // Get the user's first name (for making a reservation)
  private static String getFirstName() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter your first name: ");
    String firstName = "'" + input.next() + "'";
    return firstName;
  }

  // Get the user's last name (for making a reservation)
  private static String getLastName() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter your last name: ");
    String lastName = "'" + input.next() + "'";
    return lastName;
  }

  // Get the number of adults for a reservation
  private static int getNumAdults() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter number of adults: ");
    int numAdults = input.nextInt();
    return numAdults;
  }

  // Get the number of children for a reservation
  private static int getNumChildren() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter number of children: ");
    int numChildren = input.nextInt();
    return numChildren;
  }

  // get discount for a room reservation
  private static String getDiscount() {
    Scanner input = new Scanner(System.in);
    System.out.print("Enter discount (AAA or AARP, if applicable): ");
    String dsName = input.nextLine().toUpperCase();
    return dsName;
  }

}