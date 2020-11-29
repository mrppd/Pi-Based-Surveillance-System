package com.example.pimonitor;

import android.content.DialogInterface;
import android.net.Uri;
import android.os.AsyncTask;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.MediaController;
import android.widget.Toast;
import android.app.ProgressDialog;
import android.content.pm.ActivityInfo;
import android.view.WindowManager;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;


public class PiCamera extends AppCompatActivity {
    public ProgressDialog progressDialog;
    OkHttpClient client;
    MediaType JSON;
    WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pi_camera);

        getSupportActionBar().setDisplayShowHomeEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        getSupportActionBar().setTitle("PiCamera Feed");

        client = new OkHttpClient();
        JSON = MediaType.parse("application/json; charset=utf-8");
        /*
        VideoView videoView = (VideoView) findViewById(R.id.videoView);

        //set the media controller
        //MediaController mediaController = new MediaController(this);
        //mediaController.setAnchorView(videoView);

        //set the url of the video
        Uri uri = Uri.parse("http://ppdstream.serveo.net/?action=stream");

        //setting the video
        //videoView.setMediaController(mediaController);
        videoView.setVideoURI(uri);
        videoView.start();
        */

        webView = (WebView) findViewById(R.id.webView);
        webView.setWebViewClient(new WebViewClient());
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setSupportZoom(true);
        webSettings.setAppCacheEnabled(true);
        //webView.loadUrl("http://ppdstream.serveo.net/?action=stream");

        try {
            makeGetRequestCameraOn("https://ppdweb.serveo.net/startCamera?width=320&height=500");
        } catch (IOException e) {
            e.printStackTrace();
        }

    }


    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if(id==android.R.id.home){
            try {
                makeGetRequestCameraOff("https://ppdweb.serveo.net/stopCamera");
            } catch (IOException e) {
                e.printStackTrace();
            }
            this.finish();
        }
        return super.onOptionsItemSelected(item);
    }




    public void makeGetRequestCameraOn(String url) throws IOException {
        GetTaskCameraOn task = new GetTaskCameraOn(url);
        task.execute();
    }

    public class GetTaskCameraOn extends AsyncTask<Object,Void, JSONObject> {
        private Exception exception;
        String web_url;

        public GetTaskCameraOn(String url)
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

                                PiCamera.this.finish();
                                Log.v("alert", "clicked yes");
                                break;
                        }
                    }
                };
                AlertDialog.Builder builder = new AlertDialog.Builder(PiCamera.this);
                builder.setMessage("Unable to connect. Do you want to continue?").setPositiveButton("Yes", dialogClickListener)
                        .setNegativeButton("No", dialogClickListener).setCancelable(false).show();
                progressDialog.dismiss();
                return;
            }

            try {
                if(getResponse.has("stream_address") && getResponse.has("camera_status"))
                {
                    String stream_address = getResponse.get("stream_address").toString();
                    webView.loadUrl(stream_address);
                    Toast.makeText(PiCamera.this, "Connected to Camera", Toast.LENGTH_SHORT).show();
                    progressDialog.dismiss();
                   // takePassword();
                }
                else {
                    Toast.makeText(PiCamera.this, "Error occured.", Toast.LENGTH_SHORT).show();
                    progressDialog.dismiss();
                }
            } catch (JSONException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
                Toast.makeText(PiCamera.this, "Error occured.", Toast.LENGTH_SHORT).show();
                progressDialog.dismiss();
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
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // This code will always run on the UI thread, therefore is safe to modify UI elements.
                        progressDialog = ProgressDialog.show(PiCamera.this, "Please Wait", "Connecting...");
                    }
                });

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





    public void makeGetRequestCameraOff(String url) throws IOException {
        GetTaskCameraOff task = new GetTaskCameraOff(url);
        task.execute();
    }

    public class GetTaskCameraOff extends AsyncTask<Object,Void, JSONObject> {
        private Exception exception;
        String web_url;

        public GetTaskCameraOff(String url)
        {
            web_url = url;
        }

        @Override
        protected void onPostExecute(JSONObject getResponse) {
            if(getResponse==null)
            {
                //PiCamera.this.finish();
                //progressDialog.dismiss();
                return;
            }
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
                        progressDialog = ProgressDialog.show(PiCamera.this, "Please Wait", "Connecting...");
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


    @Override
    public void onResume() {
        super.onResume();  // Always call the superclass method first
        try {
            makeGetRequestCameraOn("https://ppdweb.serveo.net/startCamera?width=320&height=500");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    @Override
    public void onPause() {
        super.onPause();  // Always call the superclass method first
        try {
            makeGetRequestCameraOff("https://ppdweb.serveo.net/stopCamera");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
