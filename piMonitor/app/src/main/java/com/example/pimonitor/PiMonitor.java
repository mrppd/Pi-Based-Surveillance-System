package com.example.pimonitor;

import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.AsyncTask;
import android.os.Handler;
import android.support.v4.app.NavUtils;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.WindowManager;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class PiMonitor extends AppCompatActivity {
    public ProgressDialog progressDialog;
    OkHttpClient client;
    MediaType JSON;
    TextView textTemperature, textHumidity, textMovement, textSoundState, textLightCondition;
    Timer timer;
    TimerTask timerTask;
    Handler mTimerHandler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pi_monitor);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        getSupportActionBar().setTitle("PiMonitor");

        getSupportActionBar().setDisplayShowHomeEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        textTemperature = (TextView) findViewById(R.id.textTemperature);
        textHumidity = (TextView) findViewById(R.id.textHumidity);
        textMovement = (TextView) findViewById(R.id.textMovement);
        textSoundState = (TextView) findViewById(R.id.textSoundState);
        textLightCondition = (TextView) findViewById(R.id.textLightCondition);

        client = new OkHttpClient();
        JSON = MediaType.parse("application/json; charset=utf-8");



        timer = new Timer();
        mTimerHandler = new Handler();
        timerTask = new TimerTask() {
            @Override
            public void run() {

                mTimerHandler.post(new Runnable() {
                    public void run(){
                        //TODO
                        Log.v("timer", "working");
                        try {
                            makeGetRequestReadSensor("https://ppdweb.serveo.net/updateMonitor");
                        } catch (IOException e) {
                            e.printStackTrace();
                        }

                    }
                });
            }
        };
        //timer.schedule(timerTask, 1000L, );
        timer.scheduleAtFixedRate(timerTask,1000,5000);

    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if(id==android.R.id.home){
            if(timer != null) {
                timer.cancel();
                timer.purge();
                timer = null;
            }
            this.finish();
        }
        return super.onOptionsItemSelected(item);
    }




    public void makeGetRequestReadSensor(String url) throws IOException {
        PiMonitor.GetTaskReadSensor task = new PiMonitor.GetTaskReadSensor(url);
        task.execute();
    }

    public class GetTaskReadSensor extends AsyncTask<Object,Void, JSONObject> {
        private Exception exception;
        String web_url;

        public GetTaskReadSensor(String url)
        {
            web_url = url;
        }


        @Override
        protected void onPostExecute(JSONObject getResponse) {
            if(getResponse==null)
            {
                DialogInterface.OnClickListener dialogClickListener = new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        switch (which){
                            case DialogInterface.BUTTON_POSITIVE:
                                //Yes button clicked


                                Log.v("alert", "clicked yes");
                                break;

                            case DialogInterface.BUTTON_NEGATIVE:
                                //Yes button clicked

                                PiMonitor.this.finish();
                                Log.v("alert", "clicked yes");
                                break;
                        }
                    }
                };
                AlertDialog.Builder builder = new AlertDialog.Builder(PiMonitor.this);
                builder.setMessage("Unable to connect! Do you want to continue?").setPositiveButton("Yes", dialogClickListener)
                        .setNegativeButton("No", dialogClickListener).setCancelable(false).show();
                //progressDialog.dismiss();
                return;
            }

            try {
                if(getResponse.has("time"))
                {
                    String humidity = getResponse.get("humid").toString();
                    String temperature = getResponse.get("temp").toString();
                    String movement = getResponse.get("video_state").toString();
                    String sound_state = getResponse.get("audio_state").toString();
                    //String head_count = getResponse.get("head_count").toString();
                    String light_condition = getResponse.get("light_condition").toString();
                    String time = getResponse.get("time").toString();

                    textTemperature.setText(temperature+"'C");
                    textHumidity.setText(humidity+"%");
                    textMovement.setText(movement);
                    textSoundState.setText(sound_state);
                    textLightCondition.setText(light_condition);

                    //Toast.makeText(PiMonitor.this, "Showing live sensor data.", Toast.LENGTH_SHORT).show();
                    //progressDialog.dismiss();
                    // takePassword();
                }
                else {
                    Toast.makeText(PiMonitor.this, "Error occured.", Toast.LENGTH_SHORT).show();
                    //progressDialog.dismiss();
                }
            } catch (JSONException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
                Toast.makeText(PiMonitor.this, "Error occured.", Toast.LENGTH_SHORT).show();
               // progressDialog.dismiss();
            }
            //progressDialog.dismiss();
            //Log.v("httpmsg", getResponse);
        }

        public String get(String url) throws IOException {
            Request request = new Request.Builder()
                    .url(url)
                    .build();

            Response response = client.newCall(request).execute();
            return response.body().string();
        }

        @Override
        protected JSONObject doInBackground(Object... params) {
            try {
                /*
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // This code will always run on the UI thread, therefore is safe to modify UI elements.
                        progressDialog = ProgressDialog.show(PiMonitor.this, "Please Wait", "Connecting...");
                    }
                });
                */

                String getResponse = get(web_url);
                Log.v("httpgetpass", web_url);
                try {
                    JSONObject jsonObject = new JSONObject(getResponse);
                    Log.v("httpgetpass", getResponse);
                    return jsonObject;
                } catch (JSONException jsonObjectError) {
                    //e.printStackTrace();
                    return null;
                }
            } catch (Exception responseObjectError) {
                this.exception = responseObjectError;
                return null;
            }
        }
    }
}
