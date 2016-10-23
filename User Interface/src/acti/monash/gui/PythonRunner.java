package acti.monash.gui;

import java.awt.BorderLayout;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.SwingWorker;

public class PythonRunner
{
	public static String pythonLocation = "python/";
	public boolean isSuccessful = true;
	private static boolean donePythonLoading = false;

	public static JDialog progressDialog;
	public static JLabel processLabel;

	public PythonRunner()
	{
		JProgressBar progressBar;
		JPanel panel;

		progressBar = new JProgressBar(0, 100);
		progressBar.setIndeterminate(true);
		processLabel = new JLabel("Processing Data...");
		processLabel.setOpaque(false);

		panel = new JPanel(new BorderLayout(5, 5));
		panel.add(processLabel, BorderLayout.PAGE_START);
		panel.add(progressBar, BorderLayout.CENTER);
		panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
		processLabel.setBackground(panel.getBackground());

		progressDialog = new JDialog(GuiFrame.frame, "Acti | Monash", true);
		progressDialog.getContentPane().add(panel);
		progressDialog.setResizable(false);
		progressDialog.setSize(200, 90);
		progressDialog.setLocationRelativeTo(null);
		progressDialog.setAlwaysOnTop(false);
	}

	public void execute()
	{
		String errorMessage = "";
		try
		{
			processLabel.setText("Processing Data...");
			GraphImages.garbageCollect();
			File crashFile = new File(pythonLocation + "crashes.txt");
			File errorLog = new File(pythonLocation + "Error_Log.txt");
			File statusFile = new File(pythonLocation + "ProgramStatus.txt");
			File fileWorked = new File(pythonLocation + "worked.txt");
			if (crashFile.exists()) crashFile.delete();
			if (errorLog.exists()) errorLog.delete();
			if (fileWorked.exists()) fileWorked.delete();
			if (statusFile.exists()) statusFile.delete();

			ProcessBuilder pb = new ProcessBuilder("python", "main.py");
			pb.directory(new File(pythonLocation));
			pb.redirectError();

			SwingWorker worker = new SwingWorker()
			{

				@Override
				protected void done()
				{
					progressDialog.dispose();
				}

				@Override
				protected void process(List chunks)
				{

				}

				@Override
				protected Object doInBackground() throws Exception
				{
					Thread.sleep(1000);
					Process p = pb.start();
					while (p.isAlive())
					{
						processLabel.setText("Processing Graph " + GraphImages.graphFileCount());
						Thread.sleep(1000);
					}
					this.publish();
					this.done();
					return null;
				}
			};
			worker.execute();
			pb.redirectError(errorLog);
			progressDialog.setVisible(true);

			if (crashFile.exists())
			{
				BufferedReader br = new BufferedReader(new FileReader(crashFile));
				String line;
				while ((line = br.readLine()) != null)
					errorMessage += (line + "\n");
				br.close();
			}
			if (errorMessage.trim().equals("None")) errorMessage = "";
			if (crashFile.exists() && errorMessage.equals(""))
			{
				BufferedReader br = new BufferedReader(new FileReader(errorLog));
				String line;
				while ((line = br.readLine()) != null)
					errorMessage += (line + "\n");
				br.close();
			}
			if (errorMessage.trim().equals("None")) errorMessage = "";

			fileWorked = new File(pythonLocation + "worked.txt");
			if (!fileWorked.exists() && errorMessage.equals("")) errorMessage = "Data processing was unsuccessful";
			fileWorked.delete();

			if (statusFile.exists())
			{
				BufferedReader br = new BufferedReader(new FileReader(statusFile));
				String line;
				String status = "";
				while ((line = br.readLine()) != null)
					status += line;
				br.close();
				if (status.trim().equals("crashed")) errorMessage = "Unexpected Error: Please send Error_Log.txt to the devalopers\n\n" + errorMessage;
			}
		}
		catch (Exception e)
		{
			errorMessage = "Unexpected Error\n\n" + e.getMessage();
			e.printStackTrace();
		}
		errorMessage = errorMessage.trim();

		if (!errorMessage.equals(""))
		{
			JOptionPane.showMessageDialog(GuiFrame.frame, errorMessage, "Error", JOptionPane.ERROR_MESSAGE);
			this.isSuccessful = false;
		}
		else this.isSuccessful = true;

		this.isSuccessful = true;

		GraphImages.load();
	}
}
