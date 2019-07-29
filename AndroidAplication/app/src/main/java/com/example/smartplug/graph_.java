package com.example.smartplug;

import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;

import com.jjoe64.graphview.DefaultLabelFormatter;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.charset.Charset;
import java.text.ParseException;

public class graph_ extends AppCompatActivity {
    String power[];
    String current[];
    String time[];


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_graph_);

         Graph1 g2=new Graph1();
            g2.execute();
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    public void rough() throws ParseException {
//        Date[] date;
//        DateFormat sdf = null;
//        date=new Date[10];
//        for(int i=0;i<10;i++)
//        {
//            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.N) {
//                sdf = new SimpleDateFormat("hh:mm:ss");
//            }
//            date[i] = sdf.parse(time[i]);
//
//            System.out.println("Time:" + sdf.format(date[i])+"jgj"+date[i]);
//        }
//        System.out.println("above");
        GraphView graphView = (GraphView) findViewById(R.id.graphp);
        graphView.getGridLabelRenderer().setLabelFormatter(new DefaultLabelFormatter() {
            @Override
            public String formatLabel(double value, boolean isValueX) {
                if (isValueX) {
                    // show normal x values
                    return time[(int) value];
                } else {
                    // show currency for y values
                    return power[(int)value]+"";
                }
            }
        });
        LineGraphSeries<DataPoint> series = new LineGraphSeries<DataPoint>(new DataPoint[] {
                new DataPoint(0, 0),
                new DataPoint(1,1),
                new DataPoint(2,2),
                new DataPoint(3,3),
                new DataPoint(4,1),
        });
        graphView.addSeries(series);

        GraphView graphView1 = (GraphView) findViewById(R.id.graph);
        graphView1.getGridLabelRenderer().setLabelFormatter(new DefaultLabelFormatter() {
            @Override
            public String formatLabel(double value, boolean isValueX) {
                if (isValueX) {
                    // show normal x values
                    return time[(int) value];
                } else {
                    // show currency for y values
                    return current[(int)value]+"";
                }
            }
        });
        LineGraphSeries<DataPoint> series1 = new LineGraphSeries<DataPoint>(new DataPoint[] {
                new DataPoint(0, 0),
                new DataPoint(1,1),
                new DataPoint(2,2),
                new DataPoint(3,3),
                new DataPoint(4,1),
        });
        graphView1.addSeries(series1);

        System.out.println("kkkkkkkkk");
    }




    public class Graph1 extends AsyncTask<Void,Void,Void> {



        @RequiresApi(api = Build.VERSION_CODES.KITKAT)
        @Override
        protected Void doInBackground(Void... voids) {
            try {
                URL url = new URL("https://sriki007.pythonanywhere.com/androidgetgraphdata");
                HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
                InputStream inputStream = httpURLConnection.getInputStream();
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream, Charset.defaultCharset(
                        )));

                String line="";
                String data="";

                while(line != null){
                    line = bufferedReader.readLine();
                    data=data+line;
                    if(line==null)
                    {
                        break;
                    }
                }

                String words = data.replace("&#39;","");
                char[] word=words.toCharArray();

                int i=0;
                String j="";
                int k=0;
                String graphvalue[];
                graphvalue=new String[100];

                time=new String[10];
                current=new String[10];
                power= new String[10];


                //for convert of string to array.
                while(true)
                {
                    if(word[i]=='[')
                    {
                        i+=1;
                        continue;
                    }

                    else if(word[i]==']')
                    {
                        graphvalue[k]=j;
                        k=k+1;
                        j="";
                        break;
                    }
                    else if(word[i]==',')
                    {
                        i+=1;
                        graphvalue[k]=j;
                        k=k+1;
                        j="";
                        continue;
                    }
                    else
                    {

                        j=j+word[i];

                        i+=1;
                    }
                }

                for(i=0;i<10;i++)
                {
//                    power[i]=Float.valueOf(graphvalue[i]);
                    power[i]=(graphvalue[i]);

                }
                k=0;
                for(i=10;i<20;i++)
                {
                    current[k]=(graphvalue[i]);
                    k++;
                }
                k=0;
                for(i=20;i<30;i++)
                {
                    time[k]=(graphvalue[i]);
                    k++;
                }


            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            return null;
        }



        @Override
        protected void onPostExecute(Void aVoid) {
            super.onPostExecute(aVoid);
            try {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                    rough();
                }
            } catch (ParseException e) {
                e.printStackTrace();
            }
        }

    }





}
